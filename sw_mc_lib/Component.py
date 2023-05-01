from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import chain
from typing import Optional, Type

from .Input import Input
from .NumberProperty import NumberProperty
from .Position import Position
from .Types import ComponentType
from .XMLElement import XMLElement
from .XMLParser import XMLParserElement

INNER_TO_XML_RESULT = tuple[dict[str, str], list[XMLParserElement]]


class Component(XMLElement, ABC):
    """
    A generic Component
    """

    width: float = 1

    def __init__(
        self,
        component_type: ComponentType,
        component_id: int,
        position: Position,
        height: float,
    ):
        self.type: ComponentType = component_type
        self.component_id: int = component_id
        self.position: Position = position
        self.height: float = height

    @staticmethod
    def _basic_in_parsing(
        element: XMLParserElement,
    ) -> tuple[int, Position, dict[str, Input], dict[str, NumberProperty]]:
        component_id: int = int(element.attributes.get("id", "0"))
        position: Position = Position()
        inputs: dict[str, Input] = {}
        properties: dict[str, NumberProperty] = {}
        for child in element.children:
            if child.tag == "pos":
                position = Position.from_xml(child)
            elif child.tag.startswith("in"):
                input: Input = Input.from_xml(child)
                if input.component_id > 0:
                    inputs[input.index] = input
            else:
                properties[child.tag] = NumberProperty.from_xml(child)
        return component_id, position, inputs, properties

    @abstractmethod
    def _inner_to_xml(self) -> tuple[dict[str, str], list[XMLParserElement]]:
        ...

    def to_xml(self) -> XMLParserElement:
        object_element = XMLParserElement("object", {"id": str(self.component_id)}, [])
        inner_attributes, inner_children = self._inner_to_xml()
        object_element.attributes.update(inner_attributes)
        object_element.children = inner_children
        return XMLParserElement("c", {"type": str(self.type.value)}, [object_element])

    def to_state_xml(self, index: int) -> XMLParserElement:
        """
        Convert this Component to a XML state entity

        :param index: The zero based index of the entity
        :return: XML state representation
        """
        c_element: XMLParserElement = XMLParserElement(
            f"c{index}", {"id": str(self.component_id)}
        )
        inner_attributes, inner_children = self._inner_to_xml()
        c_element.attributes.update(inner_attributes)
        c_element.children = inner_children
        return c_element

    def _pos_in_to_xml(
        self,
        *inputs: Optional[Input],
        named_inputs: Optional[dict[str, Optional[Input]]] = None,
        properties: Optional[dict[str, NumberProperty]] = None,
    ) -> list[XMLParserElement]:
        """
        Turn the position and inputs into an element. Will strip all None inputs. Will also rename all numbered inputs
        to their according supplied index, and all named inputs to the supplied name.

        :param inputs: Array of inputs, the order is important, as it defines overrides
        :param named_inputs: Inputs by name, used for overrides
        :param properties: Properties by name
        :return: XML elements for all relevant children
        """
        named_inputs = named_inputs or {}
        properties = properties or {}
        children: list[XMLParserElement] = [self.position.to_xml()]
        for i, input in chain(enumerate(inputs), named_inputs.items()):
            if input is not None:
                if isinstance(i, int):
                    input.index = str(i + 1)
                else:
                    assert isinstance(i, str)
                    input.index = i
                children.append(input.to_xml())
        for name, property in properties.items():
            property.name = name
            children.append(property.to_xml())
        return children

    @staticmethod
    def from_xml(element: XMLParserElement) -> Component:
        # pylint: disable=too-many-statements
        component_type: ComponentType = ComponentType(
            int(element.attributes.get("type", "0"))
        )
        element_class: Optional[Type[Component]] = None
        match component_type:
            case ComponentType.Abs:
                element_class = Abs
            case ComponentType.Add:
                element_class = Add
            case ComponentType.AND:
                element_class = AND
            case ComponentType.ArithmeticFunction1In:
                element_class = ArithmeticFunction1In
            case ComponentType.ArithmeticFunction3In:
                element_class = ArithmeticFunction3In
            case ComponentType.ArithmeticFunction8In:
                element_class = ArithmeticFunction8In
            case ComponentType.AudioSwitchbox:
                element_class = AudioSwitchbox
            case ComponentType.Blinker:
                element_class = Blinker
            case ComponentType.BooleanFunction4In:
                element_class = BooleanFunction4In
            case ComponentType.BooleanFunction8In:
                element_class = BooleanFunction8In
            case ComponentType.Capacitor:
                element_class = Capacitor
            case ComponentType.Clamp:
                element_class = Clamp
            case ComponentType.CompositeBinaryToNumber:
                element_class = CompositeBinaryToNumber
            case ComponentType.CompositeReadBoolean:
                element_class = CompositeReadBoolean
            case ComponentType.CompositeReadNumber:
                element_class = CompositeReadNumber
            case ComponentType.CompositeSwitchbox:
                element_class = CompositeSwitchbox
            case ComponentType.CompositeWriteBoolean:
                element_class = CompositeWriteBoolean
            case ComponentType.CompositeWriteNumber:
                element_class = CompositeWriteNumber
            case ComponentType.ConstantNumber:
                element_class = ConstantNumber
            case ComponentType.ConstantOn:
                element_class = ConstantOn
            case ComponentType.Delta:
                element_class = Delta
            case ComponentType.Divide:
                element_class = Divide
            case ComponentType.Equal:
                element_class = Equal
            case ComponentType.GreaterThan:
                element_class = GreaterThan
            case ComponentType.JKFlipFlop:
                element_class = JKFlipFlop
            case ComponentType.LessThan:
                element_class = LessThan
            case ComponentType.LuaScript:
                element_class = LuaScript
            case ComponentType.MemoryRegister:
                element_class = MemoryRegister
            case ComponentType.Modulo:
                element_class = Modulo
            case ComponentType.Multiply:
                element_class = Multiply
            case ComponentType.NAND:
                element_class = NAND
            case ComponentType.NOR:
                element_class = NOR
            case ComponentType.NOT:
                element_class = NOT
            case ComponentType.NumberToCompositeBinary:
                element_class = NumberToCompositeBinary
            case ComponentType.NumericalJunction:
                element_class = NumericalJunction
            case ComponentType.NumericalSwitchbox:
                element_class = NumericalSwitchbox
            case ComponentType.OR:
                element_class = OR
            case ComponentType.PIDController:
                element_class = PIDController
            case ComponentType.PIDControllerAdvanced:
                element_class = PIDControllerAdvanced
            case ComponentType.PropertyDropdown:
                element_class = PropertyDropdown
            case ComponentType.PropertyNumber:
                element_class = PropertyNumber
            case ComponentType.PropertySlider:
                element_class = PropertySlider
            case ComponentType.PropertyText:
                element_class = PropertyText
            case ComponentType.PropertyToggle:
                element_class = PropertyToggle
            case ComponentType.Pulse:
                element_class = Pulse
            case ComponentType.PushToToggle:
                element_class = PushToToggle
            case ComponentType.SRLatch:
                element_class = SRLatch
            case ComponentType.Subtract:
                element_class = Subtract
            case ComponentType.Threshold:
                element_class = Threshold
            case ComponentType.TimerRTF:
                element_class = TimerRTF
            case ComponentType.TimerRTO:
                element_class = TimerRTO
            case ComponentType.TimerTOF:
                element_class = TimerTOF
            case ComponentType.TimerTON:
                element_class = TimerTON
            case ComponentType.TooltipBoolean:
                element_class = TooltipBoolean
            case ComponentType.TooltipNumber:
                element_class = TooltipNumber
            case ComponentType.UpDownCounter:
                element_class = UpDownCounter
            case ComponentType.VideoSwitchbox:
                element_class = VideoSwitchbox
            case ComponentType.XOR:
                element_class = XOR
        if not element_class:
            raise NotImplementedError(
                f"No Component found for component type {component_type}"
            )
        return element_class.from_xml(element)


from .Components import *  # noqa: ignore=F403 pylint: disable=wildcard-import,wrong-import-position
