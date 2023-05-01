import unittest

from sw_mc_lib.XMLParser import XMLParser, XMLParserElement, parse


class TestXMLParser(unittest.TestCase):
    def test_unfinished_element(self) -> None:
        with self.assertRaises(NameError):
            parse("<abc ")
        with self.assertRaises(NameError):
            parse("<abc")

    def test_unfinished_string(self) -> None:
        with self.assertRaises(NameError):
            parse('<abc def="ghi')

    def test_unclosed_element(self) -> None:
        with self.assertRaises(NameError):
            parse("<abc>def")

    def test_wrong_closed_element(self) -> None:
        with self.assertRaises(NameError):
            parse("<abc></def>")

    def test_empty_element(self) -> None:
        res: XMLParserElement = parse("<abc/>")
        self.assertEqual(res, XMLParserElement("abc"))
        self.assertNotEqual(res, XMLParserElement("def"))
        self.assertNotEqual(res, "abc")

    def test_element_with_attributes(self) -> None:
        res: XMLParserElement = parse('<abc def="ghi" jkl="mno"/>')
        self.assertEqual(res, XMLParserElement("abc", {"def": "ghi", "jkl": "mno"}))

    def test_element_with_children(self) -> None:
        res: XMLParserElement = parse("<abc><def><ghi/></def></abc>")
        self.assertEqual(
            res,
            XMLParserElement(
                "abc", {}, [XMLParserElement("def", {}, [XMLParserElement("ghi")])]
            ),
        )

    def test_line_numbers(self) -> None:
        parser = XMLParser("<abc/>\n")
        parser.parse()
        self.assertEqual(parser.line, 2)
        self.assertEqual(parser.column, 1)

    def test_skipping_header(self) -> None:
        res: XMLParserElement = parse("<? ... ?><abc/>")
        self.assertEqual(res, XMLParserElement("abc"))
        with self.assertRaises(NameError):
            parse("<? abc")
