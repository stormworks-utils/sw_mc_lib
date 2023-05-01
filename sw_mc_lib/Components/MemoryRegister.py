from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .SubTypes.ResetComponent import ResetComponent


class MemoryRegister(ResetComponent):
    """
    "Remembers the input value when receiving a signal to the Set node. When the Reset node receives a signal,
    the stored number is cleared to a value that can be customised in the properties panel.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        reset_property: Optional[NumberProperty] = None,
        set_input: Optional[Input] = None,
        reset_input: Optional[Input] = None,
        number_to_store_input: Optional[Input] = None,
    ):
        super().__init__(
            ComponentType.MemoryRegister, component_id, position, 1.0, reset_property
        )
        self.set_input: Optional[Input] = set_input
        self.reset_input: Optional[Input] = reset_input
        self.number_to_store_input: Optional[Input] = number_to_store_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> MemoryRegister:
        assert element.tag == "c", f"invalid MemoryRegister {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.MemoryRegister.value
        ), f"Not an MemoryRegister {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = MemoryRegister._basic_in_parsing(
            obj
        )
        reset_property = MemoryRegister._basic_reset_parsing(properties)
        return MemoryRegister(
            component_id,
            position,
            reset_property,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(
            self.set_input, self.reset_input, self.number_to_store_input
        )
        children.extend(self._reset_to_xml())
        return {}, children
