from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class NumericalSwitchbox(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        on_value: Optional[Input],
        off_value: Optional[Input],
        switch_signal: Optional[Input],
    ):
        super().__init__(ComponentType.NumericalSwitchbox, component_id, position, 1.0)
        self.on_value: Optional[Input] = on_value
        self.off_value: Optional[Input] = off_value
        self.switch_signal: Optional[Input] = switch_signal

    @staticmethod
    def from_xml(element: XMLParserElement) -> NumericalSwitchbox:
        assert element.tag == "c", f"invalid NumericalSwitchbox {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.NumericalSwitchbox.value
        ), f"Not an NumericalSwitchbox {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = NumericalSwitchbox._basic_in_parsing(obj)
        return NumericalSwitchbox(
            component_id, position, inputs.get("1"), inputs.get("2"), inputs.get("3")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            {"1": self.on_value, "2": self.off_value, "3": self.switch_signal}
        )
