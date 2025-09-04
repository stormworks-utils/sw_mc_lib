from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.NumberProperty import NumberInput, NumberProperty
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
        min_property: NumberInput = None,
        max_property: NumberInput = None,
        value_property: NumberInput = None,
        rounding_property: NumberInput = None,
        name: str = "value",
    ):
        super().__init__(ComponentType.PropertySlider, component_id, position)
        self.rounding_property: NumberProperty = NumberProperty.from_input(
            rounding_property, "int"
        )
        self.min_property: NumberProperty = NumberProperty.from_input(
            min_property, "min"
        )
        self.max_property: NumberProperty = NumberProperty.from_input(
            max_property, "max"
        )
        self.value_property: NumberProperty = NumberProperty.from_input(
            value_property, "v"
        )
        self.name: str = name

    @property
    def height(self) -> float:
        return 0.5

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
            obj.attributes.get("name", "value"),
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {"name": self.name}, self._pos_in_to_xml(
            properties={
                "min": self.min_property,
                "max": self.max_property,
                "v": self.value_property,
                "int": self.rounding_property,
            }
        )
