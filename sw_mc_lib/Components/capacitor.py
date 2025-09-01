from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class Capacitor(Component):
    """
    Charges up when receiving an on signal, then discharges over a period of time.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        charge_input: Optional[Input] = None,
        charge_time_property: float = 1.0,
        discharge_time_property: float = 1.0,
    ):
        super().__init__(ComponentType.Capacitor, component_id, position)
        self.charge_input: Optional[Input] = charge_input
        self.charge_time_property: float = charge_time_property
        self.discharge_time_property: float = discharge_time_property

    @property
    def height(self) -> float:
        return 0.5

    @staticmethod
    def from_xml(element: XMLParserElement) -> Capacitor:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = Component._basic_in_parsing(obj)
        charge_time_property: float = float(obj.attributes.get("ct", "1"))
        discharge_time_property: float = float(obj.attributes.get("dt", "1"))
        return Capacitor(
            component_id,
            position,
            inputs.get("1"),
            charge_time_property,
            discharge_time_property,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {
            "ct": str(self.charge_time_property),
            "dt": str(self.discharge_time_property),
        }, self._pos_in_to_xml(self.charge_input)
