from __future__ import annotations
import unittest
from typing import Optional

from sw_mc_lib.Component import Component, ComponentType, Position, Input
from sw_mc_lib.XMLParser import XMLParserElement


class TestingComponent(Component):
    def __init__(self, component_id: int, position: Position, inputs: dict[str, Input]):
        super().__init__(ComponentType.Abs, component_id, position, 1.0)
        self.inputs: dict[str, Input] = inputs

    @staticmethod
    def from_xml(element: XMLParserElement) -> TestingComponent:
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs = TestingComponent._basic_in_parsing(obj)
        return TestingComponent(component_id, position, inputs)

    def _inner_to_xml(self) -> tuple[dict[str, str], list[XMLParserElement]]:
        input_list: list[Optional[Input]] = []
        named_inputs: dict[str, Optional[Input]] = {}
        for name, input in self.inputs.items():
            if name.isdigit():
                while len(input_list) < int(name):
                    input_list.append(None)
                input_list[int(name) - 1] = input
            else:
                named_inputs[name] = input
        return {}, self._pos_in_to_xml(*input_list, named_inputs=named_inputs or None)


class TestComponent(unittest.TestCase):
    def test_basic_in_parsing(self) -> None:
        elem: XMLParserElement = XMLParserElement("object", {"id": "123"})
        expected: tuple[int, Position, dict[str, Input]] = (
            123,
            Position.empty_pos(),
            {},
        )
        self.assertEqual(Component._basic_in_parsing(elem), expected)
        elem.children.append(XMLParserElement("in1", {"component_id": "1"}))
        expected[2]["1"] = Input(1, 0, "1")
        self.assertEqual(Component._basic_in_parsing(elem), expected)
        elem.children.append(XMLParserElement("in3", {"component_id": "145"}))
        expected[2]["3"] = Input(145, 0, "3")
        self.assertEqual(Component._basic_in_parsing(elem), expected)

    def test_pos_in_to_xml(self) -> None:
        pos: Position = Position(10, 5)
        test_comp: TestingComponent = TestingComponent(100, pos, {})
        expected: list[XMLParserElement] = [pos.to_xml()]
        _, children = test_comp._inner_to_xml()
        self.assertEqual(children, expected)
        test_comp.inputs["1"] = Input(10)
        expected.append(Input(10, 0, "1").to_xml())
        _, children = test_comp._inner_to_xml()
        self.assertEqual(children, expected)
        test_comp.inputs["5"] = Input(500, 2)
        expected.append(Input(500, 2, "5").to_xml())
        _, children = test_comp._inner_to_xml()
        self.assertEqual(children, expected)
        test_comp.inputs["abc"] = Input(30)
        expected.append(Input(30, 0, "abc").to_xml())
        _, children = test_comp._inner_to_xml()
        self.assertEqual(children, expected)
