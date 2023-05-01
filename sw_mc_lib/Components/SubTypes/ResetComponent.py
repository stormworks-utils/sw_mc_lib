from __future__ import annotations

from abc import ABC
from typing import Optional

from sw_mc_lib.Component import Component
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class ResetComponent(Component, ABC):
    """
    A Component that has a reset value property.
    """

    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        reset_property: Optional[NumberProperty],
        **kwargs: Optional[NumberProperty],
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.reset_property: NumberProperty = reset_property or NumberProperty("0", "r")

    @staticmethod
    def _basic_reset_parsing(
        properties: dict[str, NumberProperty]
    ) -> Optional[NumberProperty]:
        return properties.get("r")

    def _reset_to_xml(self) -> list[XMLParserElement]:
        return [self.reset_property.to_xml()]
