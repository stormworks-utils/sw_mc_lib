from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType, TimerUnit
from sw_mc_lib.XMLParser import XMLParserElement


class TimerRTO(Component):
    """
    Variable input timer. Outputs an on signal when the timer reaches its duration.
    The timer will not reset until it is signalled.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        unit_property: TimerUnit = TimerUnit.Seconds,
        timer_enable_input: Optional[Input] = None,
        duration_input: Optional[Input] = None,
        reset_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.TimerRTO, component_id, position, 0.75)
        self.timer_enable_input: Optional[Input] = timer_enable_input
        self.duration_input: Optional[Input] = duration_input
        self.reset_input: Optional[Input] = reset_input
        self.unit_property: TimerUnit = unit_property

    @staticmethod
    def from_xml(element: XMLParserElement) -> TimerRTO:
        assert element.tag == "c", f"invalid TimerRTO {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.TimerRTO.value
        ), f"Not an TimerRTO {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = TimerRTO._basic_in_parsing(obj)
        unit_property: TimerUnit = TimerUnit(int(obj.attributes.get("u", "0")))
        return TimerRTO(
            component_id,
            position,
            unit_property,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.timer_enable_input, self.duration_input)
