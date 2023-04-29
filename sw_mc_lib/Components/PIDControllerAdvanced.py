from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class PIDControllerAdvanced(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        setpoint_input: Optional[Input],
        process_variable_input: Optional[Input],
        proportional_input: Optional[Input],
        integral_input: Optional[Input],
        derivative_input: Optional[Input],
        active_input: Optional[Input],
    ):
        super().__init__(
            ComponentType.PIDControllerAdvanced, component_id, position, 2.25
        )
        self.setpoint_input: Optional[Input] = setpoint_input
        self.process_variable_input: Optional[Input] = process_variable_input
        self.proportional_input: Optional[Input] = proportional_input
        self.integral_input: Optional[Input] = integral_input
        self.derivative_input: Optional[Input] = derivative_input
        self.active_input: Optional[Input] = active_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> PIDControllerAdvanced:
        assert element.tag == "c", f"invalid PIDControllerAdvanced {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PIDControllerAdvanced.value
        ), f"Not an PIDControllerAdvanced {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            properties,
        ) = PIDControllerAdvanced._basic_in_parsing(obj)
        return PIDControllerAdvanced(
            component_id,
            position,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
            inputs.get("4"),
            inputs.get("5"),
            inputs.get("6"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            self.setpoint_input,
            self.process_variable_input,
            self.proportional_input,
            self.integral_input,
            self.derivative_input,
            self.active_input,
        )
