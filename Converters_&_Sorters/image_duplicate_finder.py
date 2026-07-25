#!/usr/bin/env python3
r"""
Find exact and visually similar PNG/JPG/JPEG images.

Exact duplicates:
    SHA-256 of the complete file.

Visually similar images:
    Perceptual hash (pHash) compared with a BK-tree, so the script does not
    need to compare every image against every other image.

The script is read-only. It never moves, renames, or deletes images.

Install:
    py -m pip install pillow imagehash

Example:
    py image_duplicate_finder.py "E:\The Stash\Imports\Images (JPG)" --output "E:\The Stash\Imports\Image Scan Results (JPG)"

Useful options:
    --threshold 6          Similarity tolerance for the default 64-bit pHash.
                           Lower = stricter. Try 4-6 first.
    --hash-size 8          pHash size. 8 means 64 bits.
    --aspect-tolerance .03 Require aspect ratios to be within 3 percent.
    --min-side 64          Ignore images smaller than 64 px on either side.
    --workers 8            Number of worker threads.
    --exact-only           Skip perceptual similarity scanning.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
    import imagehash
except ImportError:
    print(
        "Missing dependency.\n"
        "Install the required packages with:\n"
        "    py -m pip install pillow imagehash",
        file=sys.stderr,
    )
    raise SystemExit(2)


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
PRINT_LOCK = threading.Lock()


@dataclass(frozen=True)
class FileRecord:
    path: Path
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class ImageRecord:
    exact_index: int
    representative_path: Path
    phash_int: int
    phash_hex: str
    width: int
    height: int

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height if self.height else 0.0


class UnionFind:
    def __init__(self, count: int) -> None:
        self.parent = list(range(count))
        self.rank = [0] * count

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)

        if root_left == root_right:
            return

        if self.rank[root_left] < self.rank[root_right]:
            self.parent[root_left] = root_right
        elif self.rank[root_left] > self.rank[root_right]:
            self.parent[root_right] = root_left
        else:
            self.parent[root_right] = root_left
            self.rank[root_left] += 1


class BKNode:
    """BK-tree node for integer hashes using Hamming distance."""

    __slots__ = ("value", "indices", "children")

    def __init__(self, value: int, index: int) -> None:
        self.value = value
        self.indices = [index]
        self.children: dict[int, BKNode] = {}


class BKTree:
    def __init__(self) -> None:
        self.root: Optional[BKNode] = None

    @staticmethod
    def distance(left: int, right: int) -> int:
        return (left ^ right).bit_count()

    def add(self, value: int, index: int) -> None:
        if self.root is None:
            self.root = BKNode(value, index)
            return

        node = self.root
        while True:
            distance = self.distance(value, node.value)

            if distance == 0:
                node.indices.append(index)
                return

            child = node.children.get(distance)
            if child is None:
                node.children[distance] = BKNode(value, index)
                return

            node = child

    def query(self, value: int, maximum_distance: int) -> list[tuple[int, int]]:
        if self.root is None:
            return []

        matches: list[tuple[int, int]] = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            distance = self.distance(value, node.value)

            if distance <= maximum_distance:
                matches.extend((index, distance) for index in node.indices)

            low = distance - maximum_distance
            high = distance + maximum_distance

            for edge_distance, child in node.children.items():
                if low <= edge_distance <= high:
                    stack.append(child)

        return matches


def format_bytes(size: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{size} B"


def iter_image_paths(root: Path, output_directory: Path, min_side: int) -> Iterable[Path]:
    output_resolved = output_directory.resolve()

    for current_root, directory_names, file_names in os.walk(root):
        current_path = Path(current_root)

        # Do not scan the result directory if it sits inside the source tree.
        directory_names[:] = [
            name
            for name in directory_names
            if (current_path / name).resolve() != output_resolved
        ]

        for file_name in file_names:
            path = current_path / file_name
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> FileRecord:
    digest = hashlib.sha256()
    size = path.stat().st_size

    with path.open("rb") as file_handle:
        while chunk := file_handle.read(chunk_size):
            digest.update(chunk)

    return FileRecord(path=path, size_bytes=size, sha256=digest.hexdigest())


def perceptual_hash_file(
    exact_index: int,
    path: Path,
    hash_size: int,
    min_side: int,
) -> Optional[ImageRecord]:
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        width, height = image.size

        if width < min_side or height < min_side:
            return None

        # pHash works on luminance. RGB conversion also normalizes unusual modes.
        normalized = image.convert("RGB")
        hash_value = imagehash.phash(normalized, hash_size=hash_size)
        hash_hex = str(hash_value)
        hash_int = int(hash_hex, 16)

        return ImageRecord(
            exact_index=exact_index,
            representative_path=path,
            phash_int=hash_int,
            phash_hex=hash_hex,
            width=width,
            height=height,
        )


def aspect_ratios_match(left: ImageRecord, right: ImageRecord, tolerance: float) -> bool:
    if tolerance < 0:
        return True

    left_ratio = left.aspect_ratio
    right_ratio = right.aspect_ratio

    if left_ratio == 0 or right_ratio == 0:
        return False

    relative_difference = abs(left_ratio - right_ratio) / max(left_ratio, right_ratio)
    return relative_difference <= tolerance


def write_csv(path: Path, headers: list[str], rows: Iterable[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(headers)
        writer.writerows(rows)


def print_progress(prefix: str, completed: int, total: int) -> None:
    with PRINT_LOCK:
        print(f"\r{prefix}: {completed:,}/{total:,}", end="", flush=True)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect exact and visually similar PNG/JPG/JPEG images."
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Folder to scan recursively.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Result folder. Default: <source>/_image_duplicate_results",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=6,
        help="Maximum pHash Hamming distance. Default: 6. Lower is stricter.",
    )
    parser.add_argument(
        "--hash-size",
        type=int,
        default=8,
        help="pHash side length. Default 8 produces a 64-bit hash.",
    )
    parser.add_argument(
        "--aspect-tolerance",
        type=float,
        default=0.03,
        help=(
            "Maximum relative aspect-ratio difference. Default: 0.03 (3%%). "
            "Use -1 to disable."
        ),
    )
    parser.add_argument(
        "--min-side",
        type=int,
        default=0,
        help="Ignore images smaller than this many pixels on either side.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=max(2, min(16, (os.cpu_count() or 4))),
        help="Worker threads. Default: based on CPU count, capped at 16.",
    )
    parser.add_argument(
        "--exact-only",
        action="store_true",
        help="Only detect byte-identical files; skip perceptual hashing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    source = args.source.expanduser().resolve()

    if not source.is_dir():
        print(f"Source folder does not exist or is not a directory: {source}", file=sys.stderr)
        return 2

    if args.threshold < 0:
        print("--threshold must be zero or greater.", file=sys.stderr)
        return 2

    if args.hash_size < 4:
        print("--hash-size must be at least 4.", file=sys.stderr)
        return 2

    if args.min_side < 0:
        print("--min-side must be zero or greater.", file=sys.stderr)
        return 2

    if args.workers < 1:
        print("--workers must be at least 1.", file=sys.stderr)
        return 2

    output = (
        args.output.expanduser().resolve()
        if args.output
        else source / "_image_duplicate_results"
    )
    output.mkdir(parents=True, exist_ok=True)

    print(f"Scanning: {source}")
    paths = list(iter_image_paths(source, output, args.min_side))
    print(f"Found {len(paths):,} PNG/JPG/JPEG files.")

    if not paths:
        print("No supported images found.")
        return 0

    errors: list[tuple[str, str, str]] = []
    file_records: list[FileRecord] = []

    print("\nCalculating SHA-256 hashes...")
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_path = {executor.submit(sha256_file, path): path for path in paths}

        completed = 0
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                file_records.append(future.result())
            except Exception as error:
                errors.append(("sha256", str(path), repr(error)))

            completed += 1
            print_progress("SHA-256", completed, len(paths))

    print()

    exact_by_hash: dict[str, list[FileRecord]] = defaultdict(list)
    for record in file_records:
        exact_by_hash[record.sha256].append(record)

    # Stable ordering makes repeated reports easier to compare.
    exact_groups = sorted(
        exact_by_hash.values(),
        key=lambda group: str(min(record.path for record in group)).lower(),
    )

    exact_duplicate_groups = [group for group in exact_groups if len(group) > 1]

    exact_rows: list[list[object]] = []
    for group_number, group in enumerate(exact_duplicate_groups, start=1):
        group_id = f"EXACT-{group_number:06d}"
        for record in sorted(group, key=lambda item: str(item.path).lower()):
            exact_rows.append(
                [
                    group_id,
                    record.sha256,
                    record.size_bytes,
                    format_bytes(record.size_bytes),
                    str(record.path),
                ]
            )

    write_csv(
        output / "exact_duplicates.csv",
        ["group_id", "sha256", "size_bytes", "size_human", "path"],
        exact_rows,
    )

    unique_exact_groups = len(exact_groups)
    redundant_exact_files = sum(len(group) - 1 for group in exact_duplicate_groups)
    reclaimable_exact_bytes = sum(
        sum(record.size_bytes for record in group[1:])
        for group in exact_duplicate_groups
    )

    similar_pair_rows: list[list[object]] = []
    similar_group_rows: list[list[object]] = []
    skipped_small = 0
    image_records: list[ImageRecord] = []

    if not args.exact_only:
        representatives = [
            (exact_index, sorted(group, key=lambda item: str(item.path).lower())[0].path)
            for exact_index, group in enumerate(exact_groups)
        ]

        print("\nCalculating perceptual hashes...")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_item = {
                executor.submit(
                    perceptual_hash_file,
                    exact_index,
                    path,
                    args.hash_size,
                    args.min_side,
                ): (exact_index, path)
                for exact_index, path in representatives
            }

            completed = 0
            for future in as_completed(future_to_item):
                exact_index, path = future_to_item[future]
                try:
                    result = future.result()
                    if result is None:
                        skipped_small += 1
                    else:
                        image_records.append(result)
                except (UnidentifiedImageError, OSError, ValueError) as error:
                    errors.append(("phash", str(path), repr(error)))
                except Exception as error:
                    errors.append(("phash", str(path), repr(error)))

                completed += 1
                print_progress("pHash", completed, len(representatives))

        print()

        image_records.sort(key=lambda record: str(record.representative_path).lower())

        union_find = UnionFind(len(image_records))
        tree = BKTree()
        matched_pairs: list[tuple[int, int, int]] = []

        print("\nFinding visually similar images...")
        for current_index, current in enumerate(image_records):
            for previous_index, distance in tree.query(
                current.phash_int,
                args.threshold,
            ):
                previous = image_records[previous_index]

                if not aspect_ratios_match(
                    previous,
                    current,
                    args.aspect_tolerance,
                ):
                    continue

                union_find.union(previous_index, current_index)
                matched_pairs.append((previous_index, current_index, distance))

            tree.add(current.phash_int, current_index)
            print_progress("Similarity", current_index + 1, len(image_records))

        print()

        for pair_number, (left_index, right_index, distance) in enumerate(
            matched_pairs,
            start=1,
        ):
            left = image_records[left_index]
            right = image_records[right_index]

            similar_pair_rows.append(
                [
                    f"PAIR-{pair_number:07d}",
                    distance,
                    left.phash_hex,
                    right.phash_hex,
                    left.width,
                    left.height,
                    right.width,
                    right.height,
                    str(left.representative_path),
                    str(right.representative_path),
                ]
            )

        clusters: dict[int, list[int]] = defaultdict(list)
        for index in range(len(image_records)):
            clusters[union_find.find(index)].append(index)

        similar_clusters = [
            members for members in clusters.values() if len(members) > 1
        ]
        similar_clusters.sort(
            key=lambda members: str(
                min(
                    image_records[index].representative_path
                    for index in members
                )
            ).lower()
        )

        for group_number, members in enumerate(similar_clusters, start=1):
            group_id = f"SIMILAR-{group_number:06d}"

            for member_index in sorted(
                members,
                key=lambda index: str(
                    image_records[index].representative_path
                ).lower(),
            ):
                image_record = image_records[member_index]
                exact_group = exact_groups[image_record.exact_index]

                for file_record in sorted(
                    exact_group,
                    key=lambda item: str(item.path).lower(),
                ):
                    similar_group_rows.append(
                        [
                            group_id,
                            image_record.phash_hex,
                            image_record.width,
                            image_record.height,
                            len(exact_group),
                            file_record.sha256,
                            file_record.size_bytes,
                            str(file_record.path),
                        ]
                    )

        write_csv(
            output / "similar_pairs.csv",
            [
                "pair_id",
                "phash_distance",
                "left_phash",
                "right_phash",
                "left_width",
                "left_height",
                "right_width",
                "right_height",
                "left_path",
                "right_path",
            ],
            similar_pair_rows,
        )

        write_csv(
            output / "similar_groups.csv",
            [
                "group_id",
                "phash",
                "width",
                "height",
                "exact_copy_count",
                "sha256",
                "size_bytes",
                "path",
            ],
            similar_group_rows,
        )

    write_csv(
        output / "scan_errors.csv",
        ["stage", "path", "error"],
        errors,
    )

    summary_lines = [
        f"Source: {source}",
        f"Result directory: {output}",
        "",
        f"Supported images found: {len(paths):,}",
        f"Successfully SHA-256 hashed: {len(file_records):,}",
        f"Unique exact file hashes: {unique_exact_groups:,}",
        f"Exact duplicate groups: {len(exact_duplicate_groups):,}",
        f"Redundant exact copies: {redundant_exact_files:,}",
        f"Potential exact-duplicate space: {format_bytes(reclaimable_exact_bytes)}",
        f"Read/hash errors: {len(errors):,}",
    ]

    if not args.exact_only:
        similar_group_count = len(
            {row[0] for row in similar_group_rows}
        )
        summary_lines.extend(
            [
                "",
                f"pHash size: {args.hash_size}x{args.hash_size} "
                f"({args.hash_size * args.hash_size} bits)",
                f"pHash threshold: {args.threshold}",
                f"Aspect-ratio tolerance: {args.aspect_tolerance}",
                f"Images perceptually hashed: {len(image_records):,}",
                f"Images skipped by --min-side: {skipped_small:,}",
                f"Similar pairs found: {len(similar_pair_rows):,}",
                f"Similar groups found: {similar_group_count:,}",
            ]
        )

    summary_text = "\n".join(summary_lines) + "\n"
    (output / "summary.txt").write_text(summary_text, encoding="utf-8")

    print("\n" + summary_text)
    print("Reports written to:")
    print(f"  {output / 'exact_duplicates.csv'}")
    if not args.exact_only:
        print(f"  {output / 'similar_pairs.csv'}")
        print(f"  {output / 'similar_groups.csv'}")
    print(f"  {output / 'scan_errors.csv'}")
    print(f"  {output / 'summary.txt'}")
    print("\nNo files were changed, moved, or deleted.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
