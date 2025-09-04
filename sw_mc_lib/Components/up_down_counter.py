from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class UpDownCounter(Component):
    """
    Has an internal value that will increase and decrease when receiving different signals.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        up_input: Optional[Input] = None,
        down_input: Optional[Input] = None,
        reset_input: Optional[Input] = None,
        min_property: NumberInput = None,
        max_property: NumberInput = None,
        reset_property: NumberInput = None,
        increment_property: NumberInput = None,
        clamp: bool = False,
    ):
        super().__init__(ComponentType.UpDownCounter, component_id, position)
        self.up_input: Optional[Input] = up_input
        self.down_input: Optional[Input] = down_input
        self.reset_input: Optional[Input] = reset_input
        self.increment_property: NumberProperty = NumberProperty.from_input(
            increment_property, "i"
        )
        self.min_property: NumberProperty = NumberProperty.from_input(
            min_property, "min"
        )
        self.max_property: NumberProperty = NumberProperty.from_input(
            max_property, "max"
        )
        self.reset_property: NumberProperty = NumberProperty.from_input(
            reset_property, "r"
        )
        self.clamp: bool = clamp

    @property
    def height(self) -> float:
        return 1.0

    @staticmethod
    def from_xml(element: XMLParserElement) -> UpDownCounter:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Component._basic_in_parsing(obj)
        return UpDownCounter(
            component_id,
            position,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
            properties.get("min"),
            properties.get("max"),
            properties.get("r"),
            properties.get("i"),
            obj.attributes.get("m", "0") == "1",
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {"m": str(int(self.clamp))}, self._pos_in_to_xml(
            self.up_input,
            self.down_input,
            self.reset_input,
            properties={
                "min": self.min_property,
                "max": self.max_property,
                "r": self.reset_property,
                "i": self.increment_property,
            },
        )
