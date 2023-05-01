from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class ArithmeticFunction1In(Component):
    """
    Evaluates a mathematical expression with 1 input variable and outputs the result.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        function: str,
        x_input: Optional[Input] = None,
    ):
        super().__init__(
            ComponentType.ArithmeticFunction1In, component_id, position, 1.0
        )
        self.function: str = function
        self.x_input: Optional[Input] = x_input

    @staticmethod
    def from_xml(element: XMLParserElement) -> ArithmeticFunction1In:
        assert element.tag == "c", f"invalid ArithmeticFunction1In {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.ArithmeticFunction1In.value
        ), f"Not an ArithmeticFunction1In {element}"
        obj: XMLParserElement = element.children[0]
        (
            component_id,
            position,
            inputs,
            _,
        ) = ArithmeticFunction1In._basic_in_parsing(obj)
        function: str = obj.attributes.get("e", "")
        return ArithmeticFunction1In(
            component_id,
            position,
            function,
            inputs.get("1"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"e": self.function}
        children: list[XMLParserElement] = self._pos_in_to_xml(self.x_input)
        return attributes, children
