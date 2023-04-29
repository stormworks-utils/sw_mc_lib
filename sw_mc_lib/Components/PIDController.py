from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input
from sw_mc_lib.NumberProperty import NumberProperty


class PIDController(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        setpoint: Optional[Input],
        process_variable: Optional[Input],
        active: Optional[Input],
        proportional: NumberProperty,
        integral: NumberProperty,
        derivative: NumberProperty,
    ):
        super().__init__(ComponentType.PIDController, component_id, position, 1.0)
        self.setpoint: Optional[Input] = setpoint
        self.process_variable: Optional[Input] = process_variable
        self.active: Optional[Input] = active
        self.proportional: NumberProperty = proportional
        self.integral: NumberProperty = integral
        self.derivative: NumberProperty = derivative

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
        proportional: NumberProperty = properties.get("kp", NumberProperty("0", "kp"))
        integral: NumberProperty = properties.get("ki", NumberProperty("0", "ki"))
        derivative: NumberProperty = properties.get("kd", NumberProperty("0", "kd"))
        return PIDController(
            component_id,
            position,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
            proportional,
            integral,
            derivative,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(
            self.setpoint, self.process_variable, self.active
        )
        children.append(self.proportional.to_xml())
        children.append(self.integral.to_xml())
        children.append(self.derivative.to_xml())
        return {}, children
