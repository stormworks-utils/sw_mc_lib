from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType, TooltipMode
from sw_mc_lib.XMLParser import XMLParserElement


class TooltipNumber(Component):
    """
    Displays a number on this microcontroller's tooltip when it is looked at by the player on a spawned vehicle.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        label_property: str = "value",
        mode_property: TooltipMode = TooltipMode.Always,
        display_number_input: Optional[Input] = None,
        is_error_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.TooltipNumber, component_id, position, 0.75)
        self.display_number_input: Optional[Input] = display_number_input
        self.is_error_input: Optional[Input] = is_error_input
        self.label_property: str = label_property
        self.mode_property: TooltipMode = mode_property

    @staticmethod
    def from_xml(element: XMLParserElement) -> TooltipNumber:
        assert element.tag == "c", f"invalid TooltipNumber {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.TooltipNumber.value
        ), f"Not an TooltipNumber {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = TooltipNumber._basic_in_parsing(obj)
        label_property: str = obj.attributes.get("l", "")
        mode_property: TooltipMode = TooltipMode(int(obj.attributes.get("m", "0")))
        return TooltipNumber(
            component_id,
            position,
            label_property,
            mode_property,
            inputs.get("1"),
            inputs.get("2"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"l": self.label_property}
        if self.mode_property != TooltipMode.Always:
            attributes["m"] = str(self.mode_property.value)
        return attributes, self._pos_in_to_xml(
            self.display_number_input, self.is_error_input
        )
