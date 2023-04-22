from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class ArithmeticFunction8In(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        function: str,
        x: Optional[int],
        y: Optional[int],
        z: Optional[int],
        w: Optional[int],
        a: Optional[int],
        b: Optional[int],
        c: Optional[int],
        d: Optional[int],
    ):
        super().__init__(
            ComponentType.ArithmeticFunction8In, component_id, position, 2.25
        )
        self.function: str = function
        self.x: Optional[int] = x
        self.y: Optional[int] = y
        self.z: Optional[int] = z
        self.w: Optional[int] = w
        self.a: Optional[int] = a
        self.b: Optional[int] = b
        self.c: Optional[int] = c
        self.d: Optional[int] = d

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
            inputs.get(1),
            inputs.get(2),
            inputs.get(3),
            inputs.get(4),
            inputs.get(5),
            inputs.get(6),
            inputs.get(7),
            inputs.get(8),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {"e": self.function}
        children: list[XMLParserElement] = self._pos_in_to_xml(
            {
                1: self.x,
                2: self.y,
                3: self.z,
                4: self.w,
                5: self.a,
                6: self.b,
                7: self.c,
                8: self.d,
            }
        )
        return attributes, children
