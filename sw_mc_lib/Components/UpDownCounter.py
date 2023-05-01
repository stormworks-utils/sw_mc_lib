from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .SubTypes.MinMaxComponent import MinMaxComponent
from .SubTypes.ResetComponent import ResetComponent


class UpDownCounter(MinMaxComponent, ResetComponent):
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
        min_property: Optional[NumberProperty] = None,
        max_property: Optional[NumberProperty] = None,
        reset_property: Optional[NumberProperty] = None,
        increment_property: Optional[NumberProperty] = None,
    ):
        super().__init__(
            ComponentType.UpDownCounter,
            component_id,
            position,
            1.0,
            min_property,
            max_property,
            reset_property=reset_property,
        )
        self.up_input: Optional[Input] = up_input
        self.down_input: Optional[Input] = down_input
        self.reset_input: Optional[Input] = reset_input
        self.increment_property: NumberProperty = increment_property or NumberProperty(
            "0", "i"
        )

    @staticmethod
    def from_xml(element: XMLParserElement) -> UpDownCounter:
        assert element.tag == "c", f"invalid UpDownCounter {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.UpDownCounter.value
        ), f"Not an UpDownCounter {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = UpDownCounter._basic_in_parsing(
            obj
        )
        min_property, max_property = UpDownCounter._basic_min_max_parsing(properties)
        reset_property = UpDownCounter._basic_reset_parsing(properties)
        increment_property: Optional[NumberProperty] = properties.get("i")
        return UpDownCounter(
            component_id,
            position,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
            min_property,
            max_property,
            reset_property,
            increment_property,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(
            self.up_input, self.down_input, self.reset_input
        )
        children.extend(self._min_max_to_xml())
        children.extend(self._reset_to_xml())
        children.append(self.increment_property.to_xml())
        return {}, children
