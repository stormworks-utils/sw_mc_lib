from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from itertools import chain

from .XMLParser import XMLParserElement
from .Types import ComponentType
from .Position import Position
from .XMLElement import XMLElement
from .Input import Input

INNER_TO_XML_RESULT = tuple[dict[str, str], list[XMLParserElement]]


class Component(XMLElement, ABC):
    width: float = 1

    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
    ):
        self.type: ComponentType = component_type
        self.component_id: int = component_id
        self.position: Position = position
        self.height: float = height

    @staticmethod
    def _basic_in_parsing(
        element: XMLParserElement,
    ) -> tuple[int, Position, dict[str, Input]]:
        component_id: int = int(element.attributes.get("id", "0"))
        position: Optional[Position] = None
        inputs: dict[str, Input] = {}
        for child in element.children:
            if child.tag == "pos":
                position = Position.from_xml(child)
            elif child.tag.startswith("in"):
                input: Input = Input.from_xml(child)
                inputs[input.index] = input
        if not position:
            position = Position.empty_pos()
        return component_id, position, inputs

    @staticmethod
    def _basic_number_field_parsing(element: XMLParserElement, name: str) -> str:
        result: str = "0"
        for child in element.children:
            if child.tag == name:
                result = child.attributes.get("text", "0")
        return result or "0"

    @abstractmethod
    def _inner_to_xml(self) -> tuple[dict[str, str], list[XMLParserElement]]:
        ...

    def to_xml(self) -> XMLParserElement:
        object_element = XMLParserElement("object", {"id": str(self.component_id)}, [])
        inner_attributes, inner_children = self._inner_to_xml()
        object_element.attributes.update(inner_attributes)
        object_element.children = inner_children
        return XMLParserElement("c", {"type": str(self.type.value)}, [object_element])

    def _pos_in_to_xml(
        self, *inputs: Optional[Input], named_inputs: Optional[dict[str, Input]] = None
    ) -> list[XMLParserElement]:
        """
        Turn the position and inputs into an element. Will strip all None inputs. Will also rename all numbered inputs
        to their according supplied index, and all named inputs to the supplied name.
        """
        named_inputs = named_inputs or {}
        children: list[XMLParserElement] = [self.position.to_xml()]
        for i, input in chain(enumerate(inputs), named_inputs.items()):
            if input is not None:
                if isinstance(i, int):
                    input.index = str(i + 1)
                children.append(input.to_xml())
        return children
