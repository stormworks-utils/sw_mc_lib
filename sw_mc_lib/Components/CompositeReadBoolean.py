from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class CompositeReadBoolean(Component):
    """
    Reads the on/off value from a selected channel of a composite input.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        channel_property: int = 1,
        composite_signal_input: Optional[Input] = None,
    ):
        super().__init__(
            ComponentType.CompositeReadBoolean,
            component_id,
            position,
            0.5 if channel_property >= 1 else 0.75,
        )
        self.channel_property: int = channel_property
        self.composite_signal_input: Optional[Input] = composite_signal_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> CompositeReadBoolean:
        assert element.tag == "c", f"invalid CompositeReadBoolean {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.CompositeReadBoolean.value
        ), f"Not an CompositeReadBoolean {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            _,
        ) = CompositeReadBoolean._basic_in_parsing(obj)
        channel_property: int = int(obj.attributes.get("i", "0")) + 1
        return CompositeReadBoolean(
            component_id, position, channel_property, inputs.get("1")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"i": str(self.channel_property - 1)}
        children: list[XMLParserElement] = self._pos_in_to_xml(
            self.composite_signal_input
        )
        return attributes, children
