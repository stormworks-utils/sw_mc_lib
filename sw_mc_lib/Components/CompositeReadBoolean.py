from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class CompositeReadBoolean(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        channel: int,
        composite_signal: Optional[Input],
    ):
        super().__init__(
            ComponentType.CompositeReadBoolean,
            component_id,
            position,
            0.5 if channel >= 0 else 0.75,
        )
        self.channel: int = channel
        self.composite_signal: Optional[Input] = composite_signal

    @staticmethod
    def from_xml(element: XMLParserElement) -> CompositeReadBoolean:
        assert element.tag == "c", f"invalid CompositeReadBoolean {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.CompositeReadBoolean.value
        ), f"Not an CompositeReadBoolean {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = CompositeReadBoolean._basic_in_parsing(obj)
        channel: int = int(obj.attributes.get("i", "0"))
        return CompositeReadBoolean(component_id, position, channel, inputs.get("1"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"i": str(self.channel)}
        children: list[XMLParserElement] = self._pos_in_to_xml(
            {"1": self.composite_signal}
        )
        return attributes, children
