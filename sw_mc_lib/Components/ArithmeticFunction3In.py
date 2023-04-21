from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class ArithmeticFunction3In(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        function: str,
        x: Optional[int],
        y: Optional[int],
        z: Optional[int],
    ):
        super().__init__(ComponentType.ArithmeticFunction3In, component_id, position, 1.0)
        self.function: str = function
        self.x: Optional[int] = x
        self.y: Optional[int] = y
        self.z: Optional[int] = z

    @staticmethod
    def from_xml(element: XMLParserElement) -> ArithmeticFunction3In:
        assert element.tag == 'c', f'invalid ArithmeticFunction3In {element}'
        assert element.attributes.get('type', '0') == str(
            ComponentType.ArithmeticFunction3In.value
            ), f'Not an ArithmeticFunction3In {element}'
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = ArithmeticFunction3In._basic_in_parsing(obj)
        function: str = obj.attributes.get('e', '')
        return ArithmeticFunction3In(component_id, position, function, inputs.get(1), inputs.get(2), inputs.get(3))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {'e': self.function}
        children: list[XMLParserElement] = self._pos_in_to_xml({1: self.x, 2: self.y, 3: self.z})
        return attributes, children
