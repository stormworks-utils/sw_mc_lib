from __future__ import annotations

from abc import ABC

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.NumberProperty import NumberProperty


class MinMaxComponent(Component, ABC):
    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        min: NumberProperty,
        max: NumberProperty,
        **kwargs: NumberProperty,
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.min: NumberProperty = min
        self.max: NumberProperty = max

    @staticmethod
    def _basic_min_max_parsing(
        properties: dict[str, NumberProperty]
    ) -> tuple[NumberProperty, NumberProperty]:
        min: NumberProperty = properties.get("min", NumberProperty("0", "min"))
        max: NumberProperty = properties.get("max", NumberProperty("0", "max"))
        return min, max

    def _min_max_to_xml(self) -> list[XMLParserElement]:
        return [self.min.to_xml(), self.max.to_xml()]
