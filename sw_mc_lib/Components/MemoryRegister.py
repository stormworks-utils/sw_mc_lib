from __future__ import annotations

from typing import Optional

from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from .SubTypes.ResetComponent import ResetComponent


class MemoryRegister(ResetComponent):
    def __init__(
        self,
        component_id: int,
        position: Position,
        reset_text: str,
        set_input: Optional[int],
        reset_input: Optional[int],
        number_to_store: Optional[int],
    ):
        super().__init__(ComponentType.MemoryRegister, component_id, position, 1.0, reset_text)
        self.set_input: Optional[int] = set_input
        self.reset_input: Optional[int] = reset_input
        self.number_to_store: Optional[int] = number_to_store

    @staticmethod
    def from_xml(element: XMLParserElement) -> MemoryRegister:
        assert element.tag == 'c', f'invalid MemoryRegister {element}'
        assert element.attributes.get('type', '0') == str(ComponentType.MemoryRegister.value), f'Not an MemoryRegister {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = MemoryRegister._basic_in_parsing(obj)
        reset_text = MemoryRegister._basic_reset_parsing(obj)
        return MemoryRegister(component_id, position, reset_text, inputs.get(1), inputs.get(2), inputs.get(3))

    def _inner_to_xml(self) -> str:
        xml: str = self.indent(self._pos_in_to_xml({1: self.set_input, 2: self.reset_input, 3: self.number_to_store}))
        xml += self.indent(self._reset_to_xml())
        return xml