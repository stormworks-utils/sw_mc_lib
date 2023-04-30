from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Add(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        a_input: Optional[Input] = None,
        b_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.Add, component_id, position, 0.75)
        self.a_input: Optional[Input] = a_input
        self.b_input: Optional[Input] = b_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> Add:
        assert element.tag == "c", f"invalid Add {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Add.value
        ), f"Not an Add {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Add._basic_in_parsing(obj)
        return Add(component_id, position, inputs.get("1"), inputs.get("2"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.a_input, self.b_input)
