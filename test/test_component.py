import unittest
from sw_mc_lib.Component import ComponentType, Component, Position, Input
from sw_mc_lib.XMLParser import XMLParserElement


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
        expected[2]["1"] = Input("1", 1, 0)
        self.assertEqual(Component._basic_in_parsing(elem), expected)
        elem.children.append(XMLParserElement("in3", {"component_id": "145"}))
        expected[2]["3"] = Input("3", 145, 0)
        self.assertEqual(Component._basic_in_parsing(elem), expected)