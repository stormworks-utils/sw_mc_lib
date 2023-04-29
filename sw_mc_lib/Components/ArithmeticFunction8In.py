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
        x: Optional[Input],
        y: Optional[Input],
        z: Optional[Input],
        w: Optional[Input],
        a: Optional[Input],
        b: Optional[Input],
        c: Optional[Input],
        d: Optional[Input],
    ):
        super().__init__(
            ComponentType.ArithmeticFunction8In, component_id, position, 2.25
        )
        self.function: str = function
        self.x: Optional[Input] = x
        self.y: Optional[Input] = y
        self.z: Optional[Input] = z
        self.w: Optional[Input] = w
        self.a: Optional[Input] = a
        self.b: Optional[Input] = b
        self.c: Optional[Input] = c
        self.d: Optional[Input] = d

    @staticmethod
    def from_xml(element: XMLParserElement) -> ArithmeticFunction8In:
        assert element.tag == "c", f"invalid ArithmeticFunction8In {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.ArithmeticFunction8In.value
        ), f"Not an ArithmeticFunction8In {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = ArithmeticFunction8In._basic_in_parsing(obj)
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
            self.x, self.y, self.z, self.w, self.a, self.b, self.c, self.d
        )
        return attributes, children
