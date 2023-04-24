import unittest

from sw_mc_lib.XMLParser import *


class TestXMLParser(unittest.TestCase):
    def test_unfinished_element(self):
        with self.assertRaises(NameError):
            XMLParser("<abc ").parse()
        with self.assertRaises(NameError):
            XMLParser("<abc").parse()

    def test_unfinished_string(self):
        with self.assertRaises(NameError):
            XMLParser('<abc def="ghi').parse()

    def test_unclosed_element(self):
        with self.assertRaises(NameError):
            XMLParser("<abc>def").parse()

    def test_wrong_closed_element(self):
        with self.assertRaises(NameError):
            XMLParser("<abc></def>").parse()

    def test_empty_element(self):
        res: XMLParserElement = XMLParser("<abc/>").parse()
        self.assertEqual(res, XMLParserElement("abc"))
        self.assertNotEqual(res, XMLParserElement("def"))
        self.assertNotEqual(res, "abc")

    def test_element_with_attributes(self):
        res: XMLParserElement = XMLParser('<abc def="ghi" jkl="mno"/>').parse()
        self.assertEqual(res, XMLParserElement("abc", {"def": "ghi", "jkl": "mno"}))

    def test_element_with_children(self):
        res: XMLParserElement = XMLParser("<abc><def><ghi/></def></abc>").parse()
        self.assertEqual(
            res,
            XMLParserElement(
                "abc", {}, [XMLParserElement("def", {}, [XMLParserElement("ghi")])]
            ),
        )

    def test_line_numbers(self):
        parser = XMLParser("<abc/>\n")
        parser.parse()
        self.assertEqual(parser.line, 2)
        self.assertEqual(parser.column, 1)

    def test_skipping_header(self):
        res: XMLParserElement = XMLParser("<? ... ?><abc/>").parse()
        self.assertEqual(res, XMLParserElement("abc"))
        with self.assertRaises(NameError):
            XMLParser('<? abc').parse()
