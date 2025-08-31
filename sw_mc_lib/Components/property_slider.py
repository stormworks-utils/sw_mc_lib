from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.NumberProperty import NumberProperty
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement


class PropertySlider(Component):
    """
    Adds a custom slider that will be seen on the microcontroller's property panel when placed on a vehicle.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        min_property: Optional[NumberProperty] = None,
        max_property: Optional[NumberProperty] = None,
        value_property: Optional[NumberProperty] = None,
        rounding_property: Optional[NumberProperty] = None,
    ):
        super().__init__(ComponentType.PropertySlider, component_id, position, 0.5)
        self.rounding_property: NumberProperty = rounding_property or NumberProperty(
            "0", "int"
        )
        self.min_property: NumberProperty = min_property or NumberProperty("0", "min")
        self.max_property: NumberProperty = max_property or NumberProperty("0", "max")
        self.value_property: NumberProperty = value_property or NumberProperty("0", "v")

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertySlider:
        assert element.tag == "c", f"invalid PropertySlider {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PropertySlider.value
        ), f"Not an PropertySlider {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, _, properties = PropertySlider._basic_in_parsing(obj)
        return PropertySlider(
            component_id,
            position,
            properties.get("min"),
            properties.get("max"),
            properties.get("v"),
            properties.get("int"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {}, self._pos_in_to_xml(
            properties={
                "min": self.min_property,
                "max": self.max_property,
                "v": self.value_property,
                "int": self.rounding_property,
            }
        )
