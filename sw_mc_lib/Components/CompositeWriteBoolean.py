from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class CompositeWriteBoolean(Component):
    """
    Writes up to 32 on/off signals to a composite link in a single logic tick.
    Only connected channels will be modified. The number of inputs and channel to begin writing at can be configured.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        start_channel_property: int = 1,
        channel_count_property: int = 1,
        composite_signal_input: Optional[Input] = None,
        start_channel_input: Optional[Input] = None,
        channel_inputs: Optional[dict[int, Input]] = None,
    ):
        height: float = (
            0.5
            + channel_count_property * 0.25
            + (0.25 if start_channel_property == 0 else 0)
        )
        super().__init__(
            ComponentType.CompositeWriteBoolean, component_id, position, height
        )
        self.start_channel_property: int = start_channel_property
        self.channel_count_property: int = channel_count_property
        self.composite_signal_input: Optional[Input] = composite_signal_input
        self.start_channel_input: Optional[Input] = start_channel_input
        self.channel_inputs: dict[int, Input] = channel_inputs or {}

    @staticmethod
    def from_xml(element: XMLParserElement) -> CompositeWriteBoolean:
        assert element.tag == "c", f"invalid CompositeWriteBoolean {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.CompositeWriteBoolean.value
        ), f"Not an CompositeWriteBoolean {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            _,
        ) = CompositeWriteBoolean._basic_in_parsing(obj)
        start_channel_property: int = int(obj.attributes.get("offset", "0")) + 1
        channel_count_property: int = int(obj.attributes.get("count", "0"))
        channel_inputs: dict[int, Input] = {
            i: current_input for i in range(32) if (current_input := inputs.get(str(i)))
        }
        return CompositeWriteBoolean(
            component_id,
            position,
            start_channel_property,
            channel_count_property,
            inputs.get("c"),
            inputs.get("off"),
            channel_inputs,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"count": str(self.channel_count_property)}
        if self.start_channel_property != 1:
            attributes["offset"] = str(self.start_channel_property - 1)
        inputs: list[Optional[Input]] = []
        for i, current_input in self.channel_inputs.items():
            while len(inputs) < i:
                inputs.append(None)
            inputs[i - 1] = current_input
        children: list[XMLParserElement] = self._pos_in_to_xml(
            *inputs,
            named_inputs={
                "c": self.composite_signal_input,
                "off": self.start_channel_input,
            },
        )
        return {}, children
