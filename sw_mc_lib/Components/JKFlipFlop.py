from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class JKFlipFlop(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        set_input: Optional[Input] = None,
        reset_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.JKFlipFlop, component_id, position, 0.75)
        self.set_input: Optional[Input] = set_input
        self.reset_input: Optional[Input] = reset_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> JKFlipFlop:
        assert element.tag == "c", f"invalid JKFlipFlop {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.JKFlipFlop.value
        ), f"Not an JKFlipFlop {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = JKFlipFlop._basic_in_parsing(obj)
        return JKFlipFlop(component_id, position, inputs.get("1"), inputs.get("2"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.set_input, self.reset_input)
