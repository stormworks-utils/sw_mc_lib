import unittest

from sw_mc_lib.NumberProperty import NumberProperty, string_to_sw_float
from sw_mc_lib.XMLParser import XMLParserElement


class TestNumberProperty(unittest.TestCase):
    def test_from_xml(self) -> None:
        elem: XMLParserElement = XMLParserElement("prop")
        expected: NumberProperty = NumberProperty("0", "prop")
        self.assertEqual(NumberProperty.from_xml(elem), expected)
        elem.attributes["value"] = "1234.5"
        self.assertEqual(NumberProperty.from_xml(elem), expected)
        elem.attributes["text"] = "12345.67"
        expected.text = "12345.67"
        self.assertEqual(NumberProperty.from_xml(elem), expected)

    def test_to_xml(self) -> None:
        elem: NumberProperty = NumberProperty("0")
        expected: XMLParserElement = XMLParserElement(
            "temp", {"text": "0", "value": "0.0"}
        )
        self.assertEqual(elem.to_xml(), expected)
        elem.name = "abc"
        expected.tag = "abc"
        self.assertEqual(elem.to_xml(), expected)
        elem.text = "1234567.1234567"
        expected.attributes["text"] = elem.text
        expected.attributes["value"] = "1234567.125"
        self.assertEqual(elem.to_xml(), expected)

    def test_value_property(self) -> None:
        elem: NumberProperty = NumberProperty("0")
        self.assertEqual(elem.value, 0)
        elem.text = "1234"
        self.assertEqual(elem.value, 1234)
        elem.text = "1234567.1234567"
        self.assertEqual(elem.value, 1234567.125)
        elem.value = 1234
        self.assertEqual(elem.text, "1234")
        elem.value = 1234.567
        self.assertEqual(elem.text, "1234.567")

    def test_string_to_sw_float(self) -> None:
        self.assertEqual(string_to_sw_float("0"), 0)
        self.assertEqual(string_to_sw_float("1234"), 1234)
        self.assertEqual(string_to_sw_float("1234567.1234567"), 1234567.125)
        self.assertEqual(string_to_sw_float("0.123456789"), 0.123457)
        self.assertEqual(string_to_sw_float("1.23456789"), 1.234568)
