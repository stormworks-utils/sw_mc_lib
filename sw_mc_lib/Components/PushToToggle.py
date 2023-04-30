from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class PushToToggle(Component):
    def __init__(self, component_id: int, position: Position, a_input: Optional[Input]):
        super().__init__(ComponentType.PushToToggle, component_id, position, 0.5)
        self.a_input: Optional[Input] = a_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> PushToToggle:
        assert element.tag == "c", f"invalid PushToToggle {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PushToToggle.value
        ), f"Not an PushToToggle {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = PushToToggle._basic_in_parsing(obj)
        return PushToToggle(component_id, position, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.a_input)
