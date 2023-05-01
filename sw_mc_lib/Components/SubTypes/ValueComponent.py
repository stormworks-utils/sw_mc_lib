from __future__ import annotations

from abc import ABC
from typing import Optional

from sw_mc_lib.Component import Component
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class ValueComponent(Component, ABC):
    """
    A Component that has a value property.
    """

    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        value_property: Optional[NumberProperty] = None,
        **kwargs: Optional[NumberProperty],
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.value_property: NumberProperty = value_property or NumberProperty("0", "v")

    @staticmethod
    def _basic_value_parsing(
        properties: dict[str, NumberProperty]
    ) -> Optional[NumberProperty]:
        return properties.get("v")

    def _value_to_xml(self) -> list[XMLParserElement]:
        return [self.value_property.to_xml()]
