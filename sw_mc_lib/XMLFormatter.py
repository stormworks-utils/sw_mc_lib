from typing import Optional

from .XMLParser import XMLParserElement


def _escape_string(to_escape: str) -> str:
    """
    Escapes a string so that it results in valid xml. To be used like following:

    `abc<>"def\n"` -> `'abc&lt;&gt;"def\n"'`

    :param to_escape: The string that needs to be escaped
    :return: Escaped string
    """
    to_escape = to_escape.replace("&", "&amp;")
    to_escape = to_escape.replace("<", "&lt;")
    to_escape = to_escape.replace(">", "&gt;")
    if to_escape.count('"') > to_escape.count("'"):
        to_escape = to_escape.replace("'", "&apos;")
        to_escape = f"'{to_escape}'"
    else:
        to_escape = to_escape.replace('"', "&quot;")
        to_escape = f'"{to_escape}"'
    to_escape = to_escape.replace("\r\n", "\n")
    return to_escape


def _indent(to_indent: str, indentation_character: str, line_breaks: str) -> str:
    """
    Indents the string by one tab and adds a newline at the end. Will only indent lines with `\r\n`

    `<node/>` -> `\t<node/>\n`

    :param to_indent: XML block to indent
    :param indentation_character: The character(s) to use for indentation
    :param line_breaks: Either line breaks or empty string
    :return: Indented text
    """
    return (
        "\r\n".join(
            indentation_character + line for line in to_indent.rstrip().split("\r\n")
        )
        + line_breaks
    )


def _inner_format(element: XMLParserElement, indentation: str, line_breaks: str) -> str:
    xml: str = f"<{element.tag}"
    for name, value in element.attributes.items():
        xml += f" {name}={_escape_string(value)}"
    if element.children:
        xml += f">{line_breaks}"
        for child in element.children:
            xml += _indent(
                _inner_format(child, indentation, line_breaks), indentation, line_breaks
            )
        xml += f"</{element.tag}>{line_breaks}"
    else:
        xml += f"/>{line_breaks}"
    return xml


def format(
    element: XMLParserElement, indentation: Optional[str] = "\t", header: bool = False
) -> str:
    """
    Formats a XMLParserElement into a xml string. If indentation is None, there will be no line breaks or indentation.
    If header is true, it will add a xml declaration at the top of the document.

    :param element: The XML element to format
    :param indentation: The indentation character to use, `None` will not indent at all
    :param header: Whether to include the XML Header
    :return: XML string
    """
    line_breaks: str = "\r\n" if indentation is not None else ""
    indentation_character = indentation or ""
    xml: str = f'<?xml version="1.0" encoding="UTF-8"?>{line_breaks}' if header else ""
    xml += _inner_format(element, indentation_character, line_breaks)
    return xml.replace("\r\n", "\n")
