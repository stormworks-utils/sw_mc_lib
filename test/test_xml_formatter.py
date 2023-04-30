import unittest

from sw_mc_lib.XMLFormatter import format
from sw_mc_lib.XMLParser import XMLParserElement


class TestXMLFormatter(unittest.TestCase):
    def test_empty_element_formatting(self) -> None:
        res: str = format(XMLParserElement("abc"))
        self.assertEqual(res, "<abc/>\n")

    def test_element_with_attributes(self) -> None:
        res: str = format(XMLParserElement("abc", {"def": "ghi"}))
        self.assertEqual(res, '<abc def="ghi"/>\n')

    def test_element_with_children(self) -> None:
        res: str = format(
            XMLParserElement(
                "abc",
                {"def": "ghi"},
                [XMLParserElement("jkl"), XMLParserElement("mno")],
            )
        )
        self.assertEqual(res, '<abc def="ghi">\n\t<jkl/>\n\t<mno/>\n</abc>\n')

    def test_element_with_children_with_attributes(self) -> None:
        res: str = format(
            XMLParserElement(
                "abc",
                {},
                [XMLParserElement("def", {"ghi": "jkl"}, [XMLParserElement("mno")])],
            )
        )
        self.assertEqual(
            res, '<abc>\n\t<def ghi="jkl">\n\t\t<mno/>\n\t</def>\n</abc>\n'
        )

    def test_four_spaces_indent(self) -> None:
        res: str = format(
            XMLParserElement(
                "abc", {}, [XMLParserElement("def", {}, [XMLParserElement("ghi")])]
            ),
            indentation="    ",
        )
        self.assertEqual(res, "<abc>\n    <def>\n        <ghi/>\n    </def>\n</abc>\n")

    def test_empty_indent(self) -> None:
        res: str = format(
            XMLParserElement(
                "abc", {}, [XMLParserElement("def", {}, [XMLParserElement("ghi")])]
            ),
            indentation="",
        )
        self.assertEqual(res, "<abc>\n<def>\n<ghi/>\n</def>\n</abc>\n")

    def test_no_indent(self) -> None:
        res: str = format(
            XMLParserElement(
                "abc", {}, [XMLParserElement("def", {}, [XMLParserElement("ghi")])]
            ),
            indentation=None,
        )
        self.assertEqual(res, "<abc><def><ghi/></def></abc>")
        res = format(XMLParserElement("abc", {"def": "a\nbc"}), indentation=None)
        self.assertEqual(res, '<abc def="a\nbc"/>')

    def test_string_escape(self) -> None:
        res: str = format(XMLParserElement("abc", {"def": 'g\nh<>&"i'}))
        self.assertEqual(res, "<abc def='g\nh&lt;&gt;&amp;\"i'/>\n")
        res = format(XMLParserElement("abc", {"def": 'g\'h""i'}))
        self.assertEqual(res, "<abc def='g&apos;h\"\"i'/>\n")
        res = format(XMLParserElement("abc", {"def": "g\"h''i"}))
        self.assertEqual(res, "<abc def=\"g&quot;h''i\"/>\n")

    def test_attributes_with_newlines_indent(self) -> None:
        res: str = format(
            XMLParserElement("abc", {}, [XMLParserElement("def", {"def": "ghi\njkl"})])
        )
        self.assertEqual(res, '<abc>\n\t<def def="ghi\njkl"/>\n</abc>\n')
