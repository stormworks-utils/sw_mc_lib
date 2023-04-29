from __future__ import annotations

from sw_mc_lib.Component import INNER_TO_XML_RESULT
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement
from sw_mc_lib.NumberProperty import NumberProperty
from .SubTypes.MinMaxComponent import MinMaxComponent
from .SubTypes.ValueComponent import ValueComponent


class PropertySlider(MinMaxComponent, ValueComponent):
    def __init__(
        self,
        component_id: int,
        position: Position,
        min_property: NumberProperty,
        max_property: NumberProperty,
        value_property: NumberProperty,
        rounding_property: NumberProperty,
    ):
        super().__init__(
            ComponentType.PropertySlider,
            component_id,
            position,
            0.5,
            min_property,
            max_property,
            value_property=value_property,
        )
        self.rounding_property: NumberProperty = rounding_property

    @staticmethod
    def from_xml(element: XMLParserElement) -> PropertySlider:
        assert element.tag == "c", f"invalid PropertySlider {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.PropertySlider.value
        ), f"Not an PropertySlider {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, properties = PropertySlider._basic_in_parsing(
            obj
        )
        min_property, max_property = PropertySlider._basic_min_max_parsing(properties)
        value_property: NumberProperty = PropertySlider._basic_value_parsing(properties)
        rounding_property: NumberProperty = properties.get(
            "int", NumberProperty("0", "int")
        )
        return PropertySlider(
            component_id,
            position,
            min_property,
            max_property,
            value_property,
            rounding_property,
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        children: list[XMLParserElement] = self._pos_in_to_xml()
        children.extend(self._min_max_to_xml())
        children.extend(self._value_to_xml())
        children.append(self.rounding_property.to_xml())
        return {}, children
