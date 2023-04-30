import unittest

from sw_mc_lib.Input import Input, XMLParserElement


class TestInput(unittest.TestCase):
    def test_from_xml(self) -> None:
        elem: XMLParserElement = XMLParserElement("in1")
        expected: Input = Input(0, 0, "1")
        self.assertEqual(Input.from_xml(elem), expected)
        elem.attributes["component_id"] = "1234"
        expected.component_id = 1234
        self.assertEqual(Input.from_xml(elem), expected)
        elem.attributes["node_index"] = "2"
        expected.node_index = 2
        self.assertEqual(Input.from_xml(elem), expected)
        elem.tag = "inoff"
        expected.index = "off"
        self.assertEqual(Input.from_xml(elem), expected)

    def test_to_xml(self) -> None:
        current: Input = Input(123)
        expected: XMLParserElement = XMLParserElement("intemp", {"component_id": "123"})
        self.assertEqual(current.to_xml(), expected)
        current.index = "1"
        expected.tag = "in1"
        self.assertEqual(current.to_xml(), expected)
        current.node_index = 3
        expected.attributes["node_index"] = "3"
        self.assertEqual(current.to_xml(), expected)
