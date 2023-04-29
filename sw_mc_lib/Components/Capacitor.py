from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import Component, INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.Input import Input


class Capacitor(Component):
    def __init__(
        self,
        component_id: int,
        position: Position,
        charge: Optional[Input],
        charge_time: float,
        discharge_time: float,
    ):
        super().__init__(ComponentType.Capacitor, component_id, position, 1.0)
        self.charge: Optional[Input] = charge
        self.charge_time: float = charge_time
        self.discharge_time: float = discharge_time

    @staticmethod
    def from_xml(element: XMLParserElement) -> Capacitor:
        assert element.tag == "c", f"invalid Capacitor {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.Capacitor.value
        ), f"Not an Capacitor {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = Capacitor._basic_in_parsing(obj)
        charge_time: float = float(obj.attributes.get("ct", "1"))
        discharge_time: float = float(obj.attributes.get("dt", "1"))
        return Capacitor(
            component_id, position, inputs.get("1"), charge_time, discharge_time
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        attributes: dict[str, str] = {
            "ct": str(self.charge_time),
            "dt": str(self.discharge_time),
        }
        children: list[XMLParserElement] = self._pos_in_to_xml(self.charge)
        return attributes, children
