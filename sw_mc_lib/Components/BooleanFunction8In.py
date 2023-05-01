from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class BooleanFunction8In(Component):
    """
    Evaluates a logical expression with up to 8 input variables and outputs the result.
    """

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
        super().__init__(ComponentType.BooleanFunction8In, component_id, position, 2.25)
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
    def from_xml(element: XMLParserElement) -> BooleanFunction8In:
        assert element.tag == "c", f"invalid BooleanFunction8In {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.BooleanFunction8In.value
        ), f"Not an BooleanFunction8In {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            _,
        ) = BooleanFunction8In._basic_in_parsing(obj)
        function: str = obj.attributes.get("e", "")
        return BooleanFunction8In(
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
