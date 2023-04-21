from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class XOR(Component):
    def __init__(self, component_id: int, position: Position, a: Optional[int], b: Optional[int]):
        super().__init__(ComponentType.XOR, component_id, position, 0.75)
        self.a: Optional[int] = a
        self.b: Optional[int] = b

    @staticmethod
    def from_xml(element: XMLParserElement) -> XOR:
        assert element.tag == 'c', f'invalid XOR {element}'
        assert element.attributes.get('type', '0') == str(ComponentType.XOR.value), f'Not an XOR {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = XOR._basic_in_parsing(obj)
        return XOR(component_id, position, inputs.get(1), inputs.get(2))

    def _inner_to_xml(self) -> str:
        return self.indent(self._pos_in_to_xml({1: self.a, 2: self.b}))