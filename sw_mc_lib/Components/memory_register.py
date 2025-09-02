from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class MemoryRegister(Component):
    """
    "Remembers the input value when receiving a signal to the Set node. When the Reset node receives a signal,
    the stored number is cleared to a value that can be customised in the properties panel.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        reset_property: NumberInput = None,
        set_input: Optional[Input] = None,
        reset_input: Optional[Input] = None,
        number_to_store_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.MemoryRegister, component_id, position)
        self.set_input: Optional[Input] = set_input
        self.reset_input: Optional[Input] = reset_input
        self.number_to_store_input: Optional[Input] = number_to_store_input
        self.reset_property: NumberProperty = NumberProperty.from_input(
            reset_property, "r"
        )

    @property
    def height(self) -> float:
        return 1.0

    @staticmethod
    def from_xml(element: XMLParserElement) -> MemoryRegister:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Component._basic_in_parsing(obj)
        return MemoryRegister(
            component_id,
            position,
            properties.get("r"),
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            self.set_input,
            self.reset_input,
            self.number_to_store_input,
            properties={"r": self.reset_property},
        )
