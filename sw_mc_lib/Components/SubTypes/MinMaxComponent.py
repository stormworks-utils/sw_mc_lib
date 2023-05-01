from __future__ import annotations

from abc import ABC
from typing import Optional

from sw_mc_lib.Component import Component
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class MinMaxComponent(Component, ABC):
    """
    A Component that has a min and max Property.
    """

    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        min_property: Optional[NumberProperty] = None,
        max_property: Optional[NumberProperty] = None,
        **kwargs: Optional[NumberProperty],
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.min_property: NumberProperty = min_property or NumberProperty("0", "min")
        self.max_property: NumberProperty = max_property or NumberProperty("0", "max")

    @staticmethod
    def _basic_min_max_parsing(
        properties: dict[str, NumberProperty]
    ) -> tuple[Optional[NumberProperty], Optional[NumberProperty]]:
        return properties.get("min"), properties.get("max")

    def _min_max_to_xml(self) -> list[XMLParserElement]:
        return [self.min_property.to_xml(), self.max_property.to_xml()]
