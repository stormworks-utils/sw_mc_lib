from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.util import string_to_sw_float


class PIDController(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        setpoint: Optional[int],
        process_variable: Optional[int],
        active: Optional[int],
        proportional_text: str,
        integral_text: str,
        derivative_text: str,
    ):
        super().__init__(ComponentType.PIDController, component_id, position, 1.0)
        self.setpoint: Optional[int] = setpoint
        self.process_variable: Optional[int] = process_variable
        self.active: Optional[int] = active
        self.proportional_text: str = proportional_text
        self.integral_text: str = integral_text
        self.derivative_text: str = derivative_text

    @staticmethod
    def from_xml(element: XMLParserElement) -> PIDController:
        assert element.tag == "c", f"invalid PIDController {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PIDController.value
        ), f"Not an PIDController {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = PIDController._basic_in_parsing(obj)
        proportional_text: str = PIDController._basic_number_field_parsing(obj, "kp")
        integral_text: str = PIDController._basic_number_field_parsing(obj, "ki")
        derivative_text: str = PIDController._basic_number_field_parsing(obj, "kd")
        return PIDController(
            component_id,
            position,
            inputs.get(1),
            inputs.get(2),
            inputs.get(3),
            proportional_text,
            integral_text,
            derivative_text,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml(
            {1: self.setpoint, 2: self.process_variable, 3: self.active}
        )
        children.append(self._to_xml_number_field("kp", self.proportional_text))
        children.append(self._to_xml_number_field("ki", self.integral_text))
        children.append(self._to_xml_number_field("kd", self.derivative_text))
        return {}, children

    @property
    def proportional(self) -> float:
        return string_to_sw_float(self.proportional_text)

    @proportional.setter
    def proportional(self, value: float) -> None:
        self.proportional_text = str(value)

    @property
    def integral(self) -> float:
        return string_to_sw_float(self.integral_text)

    @integral.setter
    def integral(self, value: float) -> None:
        self.integral_text = str(value)

    @property
    def derivative(self) -> float:
        return string_to_sw_float(self.derivative_text)

    @derivative.setter
    def derivative(self, value: float) -> None:
        self.derivative_text = str(value)
