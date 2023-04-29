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
        min_property: NumberProperty,
        max_property: NumberProperty,
        **kwargs: NumberProperty,
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.min_property: NumberProperty = min_property
        self.max_property: NumberProperty = max_property

    @staticmethod
    def _basic_min_max_parsing(
        properties: dict[str, NumberProperty]
    ) -> tuple[NumberProperty, NumberProperty]:
        min_property: NumberProperty = properties.get("min", NumberProperty("0", "min"))
        max_property: NumberProperty = properties.get("max", NumberProperty("0", "max"))
        return min_property, max_property

    def _min_max_to_xml(self) -> list[XMLParserElement]:
        return [self.min_property.to_xml(), self.max_property.to_xml()]
