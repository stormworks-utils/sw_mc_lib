from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PushToToggle(Component):
    def __init__(self, component_id: int, position: Position, a: Optional[int]):
        super().__init__(ComponentType.PushToToggle, component_id, position, 0.5)
        self.a: Optional[int] = a

    @staticmethod
    def from_xml(element: XMLParserElement) -> PushToToggle:
        assert element.tag == 'c', f'invalid PushToToggle {element}'
        assert element.attributes.get('type', '0') == str(ComponentType.PushToToggle.value), f'Not an PushToToggle {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = PushToToggle._basic_in_parsing(obj)
        return PushToToggle(component_id, position, inputs.get(1))

    def _inner_to_xml(self) -> str:
        return self.indent(self._pos_in_to_xml({1: self.a}))
