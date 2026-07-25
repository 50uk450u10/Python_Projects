from pathlib import Path
from PIL import Image, ImageFile

#Run in PS with [py .\find_giant_images.py]

SOURCE = Path(r"e:\The Stash\Imports\Images (PNG)")
EXTENSIONS = {".png", ".jpg", ".jpeg"}
PIXEL_LIMIT = 89_478_485

ImageFile.LOAD_TRUNCATED_IMAGES = True

for path in SOURCE.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
        continue

    try:
        with Image.open(path) as image:
            width, height = image.size
            pixels = width * height

            if pixels > PIXEL_LIMIT:
                print(
                    f"{pixels:,} pixels | "
                    f"{width:,} x {height:,} | "
                    f"{path}"
                )

    except Exception as error:
        print(f"FAILED | {path} | {error}")