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
        setpoint: Optional[Input],
        process_variable: Optional[Input],
        proportional: Optional[Input],
        integral: Optional[Input],
        derivative: Optional[Input],
        active: Optional[Input],
    ):
        super().__init__(
            ComponentType.PIDControllerAdvanced, component_id, position, 2.25
        )
        self.setpoint: Optional[Input] = setpoint
        self.process_variable: Optional[Input] = process_variable
        self.proportional: Optional[Input] = proportional
        self.integral: Optional[Input] = integral
        self.derivative: Optional[Input] = derivative
        self.active: Optional[Input] = active

    @staticmethod
    def from_xml(element: XMLParserElement) -> PIDControllerAdvanced:
        assert element.tag == "c", f"invalid PIDControllerAdvanced {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PIDControllerAdvanced.value
        ), f"Not an PIDControllerAdvanced {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = PIDControllerAdvanced._basic_in_parsing(obj)
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
            {
                "1": self.setpoint,
                "2": self.process_variable,
                "3": self.proportional,
                "4": self.integral,
                "5": self.derivative,
                "6": self.active,
            }
        )
