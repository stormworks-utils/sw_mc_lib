import unittest

from sw_mc_lib.Position import Position, XMLParserElement


class TestPosition(unittest.TestCase):
    def test_from_xml(self) -> None:
        elem: XMLParserElement = XMLParserElement("pos")
        expected: Position = Position(0, 0)
        self.assertEqual(Position.from_xml(elem), expected)
        elem.attributes["x"] = "1.25"
        expected.x = 1.25
        self.assertEqual(Position.from_xml(elem), expected)
        elem.attributes["y"] = "-4.75"
        expected.y = -4.75
        self.assertEqual(Position.from_xml(elem), expected)

    def test_empty_pos(self) -> None:
        self.assertEqual(Position(), Position(0, 0))

    def test_to_xml(self) -> None:
        elem: Position = Position(0, 0)
        expected: XMLParserElement = XMLParserElement("pos")
        self.assertEqual(elem.to_xml(), expected)
        elem.x = 1.25
        expected.attributes["x"] = "1.25"
        self.assertEqual(elem.to_xml(), expected)
        elem.y = -4.0
        expected.attributes["y"] = "-4.0"
        self.assertEqual(elem.to_xml(), expected)
