from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class Delta(Component):
    def __init__(
        self, component_id: int, position: Position, value_input: Optional[Input]
    ):
        super().__init__(ComponentType.Delta, component_id, position, 0.5)
        self.value_input: Optional[Input] = value_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> Delta:
        assert element.tag == "c", f"invalid Delta {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Delta.value
        ), f"Not an Delta {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Delta._basic_in_parsing(obj)
        return Delta(component_id, position, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.value_input)
