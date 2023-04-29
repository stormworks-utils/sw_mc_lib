from __future__ import annotations

from abc import ABC

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.NumberProperty import NumberProperty


class ValueComponent(Component, ABC):
    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        value_property: NumberProperty,
        **kwargs: NumberProperty,
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.value_property: NumberProperty = value_property

    @staticmethod
    def _basic_value_parsing(properties: dict[str, NumberProperty]) -> NumberProperty:
        value_property: NumberProperty = properties.get("v", NumberProperty("0", "v"))
        return value_property

    def _value_to_xml(self) -> list[XMLParserElement]:
        return [self.value_property.to_xml()]
