# WARNING: This file will be overwritten by the build process. Do not edit directly.

from pathlib import Path


def get_blank_image() -> bytes:
    with (Path(__file__).parent / "blank_image.png").open("rb") as image:
        return image.read()
