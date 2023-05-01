from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty
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
        proportional_property: Optional[NumberProperty] = None,
        integral_property: Optional[NumberProperty] = None,
        derivative_property: Optional[NumberProperty] = None,
    ):
        super().__init__(ComponentType.PIDController, component_id, position, 1.0)
        self.setpoint_input: Optional[Input] = setpoint_input
        self.process_variable_input: Optional[Input] = process_variable_input
        self.active_input: Optional[Input] = active_input
        self.proportional_property: NumberProperty = (
            proportional_property or NumberProperty("0", "kp")
        )
        self.integral_property: NumberProperty = integral_property or NumberProperty(
            "0", "ki"
        )
        self.derivative_property: NumberProperty = (
            derivative_property or NumberProperty("0", "kd")
        )

    @staticmethod
    def from_xml(element: XMLParserElement) -> PIDController:
        assert element.tag == "c", f"invalid PIDController {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PIDController.value
        ), f"Not an PIDController {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = PIDController._basic_in_parsing(
            obj
        )
        proportional_property: Optional[NumberProperty] = properties.get("kp")
        integral_property: Optional[NumberProperty] = properties.get("ki")
        derivative_property: Optional[NumberProperty] = properties.get("kd")
        return PIDController(
            component_id,
            position,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
            proportional_property,
            integral_property,
            derivative_property,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(
            self.setpoint_input, self.process_variable_input, self.active_input
        )
        children.append(self.proportional_property.to_xml())
        children.append(self.integral_property.to_xml())
        children.append(self.derivative_property.to_xml())
        return {}, children
