# This script will bundle resource files for use in the sw_mc_lib package.
# it is intended to be run before bundling
from pathlib import Path
from base64 import b64encode

RESOURCES_DIR = Path(__file__).parent / "sw_mc_lib"
RESOURCES_FILE_PATH = RESOURCES_DIR / "_resources.py"

def bundle_resource(name: str, path: Path) -> str:
    with path.open("rb") as f:
        content = b64encode(f.read())
    return f"def get_{name}() -> bytes:\n    return b64decode({content!r})\n"

with RESOURCES_FILE_PATH.open("w") as file:
    file.write("# WARNING: This file will be overwritten by the build process. Do not edit directly.\n\n")
    file.write("from base64 import b64decode\n\n")
    file.write(bundle_resource("blank_image", RESOURCES_DIR / "blank_image.png"))
