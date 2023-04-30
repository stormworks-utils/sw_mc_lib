from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class ArithmeticFunction8In(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        function: str,
        x_input: Optional[Input] = None,
        y_input: Optional[Input] = None,
        z_input: Optional[Input] = None,
        w_input: Optional[Input] = None,
        a_input: Optional[Input] = None,
        b_input: Optional[Input] = None,
        c_input: Optional[Input] = None,
        d_input: Optional[Input] = None,
    ):
        super().__init__(
            ComponentType.ArithmeticFunction8In, component_id, position, 2.25
        )
        self.function: str = function
        self.x_input: Optional[Input] = x_input
        self.y_input: Optional[Input] = y_input
        self.z_input: Optional[Input] = z_input
        self.w_input: Optional[Input] = w_input
        self.a_input: Optional[Input] = a_input
        self.b_input: Optional[Input] = b_input
        self.c_input: Optional[Input] = c_input
        self.d_input: Optional[Input] = d_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> ArithmeticFunction8In:
        assert element.tag == "c", f"invalid ArithmeticFunction8In {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.ArithmeticFunction8In.value
        ), f"Not an ArithmeticFunction8In {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            _,
        ) = ArithmeticFunction8In._basic_in_parsing(obj)
        function: str = obj.attributes.get("e", "")
        return ArithmeticFunction8In(
            component_id,
            position,
            function,
            inputs.get("1"),
            inputs.get("2"),
            inputs.get("3"),
            inputs.get("4"),
            inputs.get("5"),
            inputs.get("6"),
            inputs.get("7"),
            inputs.get("8"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"e": self.function}
        children: list[XMLParserElement] = self._pos_in_to_xml(
            self.x_input,
            self.y_input,
            self.z_input,
            self.w_input,
            self.a_input,
            self.b_input,
            self.c_input,
            self.d_input,
        )
        return attributes, children
