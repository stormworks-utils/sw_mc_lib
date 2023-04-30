from __future__ import annotations

import string
from typing import Any, Optional


class XMLParserElement:
    def __init__(
        self,
        tag: str,
        attributes: Optional[dict[str, str]] = None,
        children: Optional[list[XMLParserElement]] = None,
    ):
        self.tag: str = tag
        self.attributes: dict[str, str] = attributes or {}
        self.children: list[XMLParserElement] = children or []

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, XMLParserElement):
            return (
                self.tag == other.tag
                and self.attributes == other.attributes
                and self.children == other.children
            )
        return False

    def __repr__(self) -> str:
        return f"XMLParserElement(tag={self.tag!r}, attributes={self.attributes!r}, children={self.children!r}"


class XMLParser:
    IDENTIFIER_CHARACTERS: str = string.ascii_letters + string.digits + "_"

    def __init__(self, content: str):
        self.content: str = content
        self.pos: int = 0
        self.line: int = 1
        self.column: int = 1
        self.current: Optional[str] = content[0]

    def advance(self) -> None:
        self.pos += 1
        if self.pos >= len(self.content):
            self.current = None
            return
        self.current = self.content[self.pos]
        if self.current == "\n":
            self.line += 1
            self.column = 0
        self.column += 1

    def skip_whitespace(self) -> None:
        while self.current and self.current.isspace():
            self.advance()

    def read_name(self) -> str:
        name: str = ""
        while self.current and self.current in self.IDENTIFIER_CHARACTERS:
            name += self.current
            self.advance()
        return name

    def read_and_unescape_string(self) -> str:
        res_str: str = ""
        assert self.current
        opening_char: str = self.current
        self.advance()
        while self.current and self.current != opening_char:
            res_str += self.current
            self.advance()
        self.advance()
        res_str = res_str.replace("&lt;", "<")
        res_str = res_str.replace("&gt;", ">")
        res_str = res_str.replace("&apos;", "'")
        res_str = res_str.replace("&quot;", '"')
        res_str = res_str.replace("&amp;", "&")
        return res_str

    def error(self, expected: str, received: str, line: int, column: int) -> None:
        raise NameError(f"Expected {expected} at {line}:{column}, got {received}")

    def eat(self, expected: str) -> None:
        if self.current == expected:
            self.advance()
        else:
            self.error(expected, self.current or "<EOL>", self.line, self.column)

    def read_element(self) -> XMLParserElement:
        tag: str = self.read_name()
        self.skip_whitespace()
        attributes: dict[str, str] = {}
        while self.current and self.current in self.IDENTIFIER_CHARACTERS:
            attr_name: str = self.read_name()
            self.eat("=")
            attr_value: str = self.read_and_unescape_string()
            attributes[attr_name] = attr_value
            self.skip_whitespace()
        children: list[XMLParserElement] = []
        if self.current == ">":
            self.eat(">")
            self.skip_whitespace()
            self.eat("<")
            while self.current and self.current != "/":
                children.append(self.read_element())
                self.skip_whitespace()
                self.eat("<")
            self.advance()
            line, column = self.line, self.column
            closing_tag: str = self.read_name()
            if closing_tag != tag:
                self.error(tag, closing_tag, line, column)
            self.eat(">")
        else:
            self.eat("/")
            self.eat(">")
        return XMLParserElement(tag, attributes, children)

    def parse(self) -> XMLParserElement:
        self.eat("<")
        if self.current == "?":
            self.advance()
            while self.current and self.current != "?":
                self.advance()
            self.eat("?")
            self.eat(">")
            self.skip_whitespace()
            self.eat("<")
        return self.read_element()
