from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class NAND(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        a: Optional[Input],
        b: Optional[Input],
    ):
        super().__init__(ComponentType.NAND, component_id, position, 0.75)
        self.a: Optional[Input] = a
        self.b: Optional[Input] = b

    @staticmethod
    def from_xml(element: XMLParserElement) -> NAND:
        assert element.tag == "c", f"invalid NAND {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.NAND.value
        ), f"Not an NAND {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = NAND._basic_in_parsing(obj)
        return NAND(component_id, position, inputs.get("1"), inputs.get("2"))

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(self.a, self.b)
