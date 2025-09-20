from pathlib import Path

from sw_mc_lib import Microcontroller, XMLFormatter
from sw_mc_lib.XMLParser import XMLParser


def read_mc_from_file(path: Path) -> Microcontroller:
    """
    Read a Microcontroller from a file

    :param path: The path to the file
    :return: The Microcontroller
    """
    with path.open("r") as file:
        content = file.read()
    element = XMLParser(content).parse()
    return Microcontroller.from_xml(element)


def write_mc_to_file(
    mc: Microcontroller, path: Path, write_thumbnail: bool = True
) -> None:
    """
    Write a Microcontroller to a file

    :param mc: The Microcontroller to write
    :param path: The path to the file
    :param write_thumbnail: Whether to write the thumbnail image
    :return: None
    """
    element = mc.to_xml()
    formatted = XMLFormatter.format(element, header=True)
    with path.open("w") as file:
        file.write(formatted)
    if write_thumbnail:
        mc.image.to_sw_png(path.with_suffix(".png"))
