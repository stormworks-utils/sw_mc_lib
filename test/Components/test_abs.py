import unittest
from sw_mc_lib.Components.Abs import Abs
from sw_mc_lib.XMLParser import XMLParser, XMLParserElement
from sw_mc_lib.Position import Position


class TestAbs(unittest.TestCase):
    def test_from_xml(self) -> None:
        elem: XMLParserElement = XMLParser(
            '<c type="14"><object id="123"/></c>'
        ).parse()
        abs_elem: Abs = Abs.from_xml(elem)
        self.assertEqual(abs_elem, Abs(123, Position.empty_pos(), None))
        elem = XMLParser(
            '<c type="14"><object id="234"><pos x="12.5"/></object></c>'
        ).parse()
        abs_elem = Abs.from_xml(elem)
        self.assertEqual(abs_elem, Abs(234, Position(12.5, 0.0), None))
        elem = XMLParser(
            '<c type="14"><object id="123"><pos x="13" y="32.75"/><in1 component_id="1"/></object></c>'
        ).parse()
        abs_elem = Abs.from_xml(elem)
        self.assertEqual(abs_elem, Abs(123, Position(13.0, 32.75), 1))
        self.assertNotEqual(abs_elem, elem)

    def test_wrong_id(self) -> None:
        elem: XMLParserElement = XMLParser('<c type="13"/>').parse()
        with self.assertRaises(AssertionError):
            Abs.from_xml(elem)
        elem = XMLParser('<d type="14"/>').parse()
        with self.assertRaises(AssertionError):
            Abs.from_xml(elem)

    def test_to_xml(self) -> None:
        elem: XMLParserElement = XMLParser(
            '<c type="14"><object id="13"><pos x="14.0" y="-5.25"/><in1 component_id="15"/></object></c>'
        ).parse()
        abs_elem: XMLParserElement = Abs.from_xml(elem).to_xml()
        self.assertEqual(abs_elem, elem)
