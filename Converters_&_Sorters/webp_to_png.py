from pathlib import Path
from PIL import Image, UnidentifiedImageError #install pillow ps [py -m pip install pillow]

SOURCE = Path(r"E:\The Stash\Reorganized\Convert Later")
OUTPUT = Path(r"E:\The Stash\Reorganized\Converted PNG")

CONVERT_EXTENSIONS = {".webp", ".avif", ".bmp", ".jfif"}

for source_file in SOURCE.rglob("*"):
    if not source_file.is_file():
        continue

    if source_file.suffix.lower() not in CONVERT_EXTENSIONS:
        continue

    relative = source_file.relative_to(SOURCE)
    output_file = (OUTPUT / relative).with_suffix(".png")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(source_file) as image:
            image.load()

            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")

            image.save(output_file, "PNG", optimize=True)
            print(f"Converted: {relative}")

    except UnidentifiedImageError:
        print(f"Not recognized as an image: {source_file}")
    except Exception as error:
        print(f"Failed: {source_file} | {error}")