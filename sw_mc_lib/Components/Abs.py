from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Abs(Component):
    def __init__(self, component_id: int, position: Position, input_number: Optional[int]):
        super().__init__(ComponentType.Abs, component_id, position, 0.5)
        self.input_number: Optional[int] = input_number

    @staticmethod
    def from_xml(element: XMLParserElement) -> Abs:
        assert element.tag == 'c', f'invalid Abs {element}'
        assert element.attributes.get('type', '0') == str(ComponentType.Abs.value), f'Not an Abs {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = Abs._basic_in_parsing(obj)
        return Abs(component_id, position, inputs.get(1))

    def _inner_to_xml(self) -> str:
        return self.indent(self._pos_in_to_xml({1: self.input_number}))
