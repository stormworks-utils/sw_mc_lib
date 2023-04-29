from __future__ import annotations

from abc import ABC

from sw_mc_lib.Component import Component
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.NumberProperty import NumberProperty


class ResetComponent(Component, ABC):
    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
        reset: NumberProperty,
        **kwargs: NumberProperty,
    ):
        super().__init__(component_type, component_id, position, height, **kwargs)
        self.reset: NumberProperty = reset

    @staticmethod
    def _basic_reset_parsing(properties: dict[str, NumberProperty]) -> NumberProperty:
        reset: NumberProperty = properties.get("r", NumberProperty("0", "r"))
        return reset

    def _reset_to_xml(self) -> list[XMLParserElement]:
        return [self.reset.to_xml()]
