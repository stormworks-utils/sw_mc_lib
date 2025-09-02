from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PIDController(Component):
    """
    A basic PID controller. The proportional, integral and derivative gains can be set in the property panel.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        setpoint_input: Optional[Input] = None,
        process_variable_input: Optional[Input] = None,
        active_input: Optional[Input] = None,
        proportional_property: NumberInput = None,
        integral_property: NumberInput = None,
        derivative_property: NumberInput = None,
    ):
        super().__init__(ComponentType.PIDController, component_id, position)
        self.setpoint_input: Optional[Input] = setpoint_input
        self.process_variable_input: Optional[Input] = process_variable_input
        self.active_input: Optional[Input] = active_input
        self.proportional_property: NumberProperty = NumberProperty.from_input(
            proportional_property, "kp"
        )
        self.integral_property: NumberProperty = NumberProperty.from_input(
            integral_property, "ki"
        )
        self.derivative_property: NumberProperty = NumberProperty.from_input(
            derivative_property, "kd"
        )

    @property
    def height(self) -> float:
        return 1.0

    @staticmethod
    def from_xml(element: XMLParserElement) -> PIDController:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Component._basic_in_parsing(obj)
        return PIDController(
            component_id,
            position,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
            properties.get("kp"),
            properties.get("ki"),
            properties.get("kd"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            self.setpoint_input,
            self.process_variable_input,
            self.active_input,
            properties={
                "kp": self.proportional_property,
                "ki": self.integral_property,
                "kd": self.derivative_property,
            },
        )
