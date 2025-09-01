import unittest

from sw_mc_lib import Input
from sw_mc_lib.Components.composite_write_boolean import CompositeWriteBoolean
from sw_mc_lib.XMLParser import XMLParserElement

from .test_utils import Position


class TestCompositeWriteBoolean(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)

    def test_simple(self) -> None:
        elem: XMLParserElement = XMLParserElement(
            "c",
            {"type": "41"},
            [
                XMLParserElement(
                    "object",
                    {"id": "1", "count": "1"},
                    [
                        XMLParserElement("pos"),
                        XMLParserElement("in1"),
                    ],
                )
            ],
        )
        expected: CompositeWriteBoolean = CompositeWriteBoolean(
            1,
            Position(0, 0),
            1,
            1,
            None,
            None,
        )
        self.assertEqual(expected, CompositeWriteBoolean.from_xml(elem))
        self.assertEqual(expected.height, 0.75)
        self.assertEqual(expected.to_xml(), elem)

    def test_multiple_channels(self) -> None:
        elem = XMLParserElement(
            "c",
            {"type": "41"},
            [
                XMLParserElement(
                    "object",
                    {"id": "2", "count": "4", "offset": "1"},
                    [
                        XMLParserElement("pos", {"x": "1.5", "y": "-0.25"}),
                        XMLParserElement("in1", {"component_id": "5"}),
                        XMLParserElement("in2", {"component_id": "6"}),
                        XMLParserElement("in3", {"component_id": "7"}),
                        XMLParserElement("in4"),
                    ],
                )
            ],
        )
        expected = CompositeWriteBoolean(
            2,
            Position(1.5, -0.25),
            2,
            4,
            None,
            None,
            {1: Input(5, index="1"), 2: Input(6, index="2"), 3: Input(7, index="3")},
        )
        self.assertEqual(expected, CompositeWriteBoolean.from_xml(elem))
        self.assertEqual(expected.height, 1.5)
        self.assertEqual(expected.to_xml(), elem)

    def test_dynamic_start_channel(self) -> None:
        elem = XMLParserElement(
            "c",
            {"type": "41"},
            [
                XMLParserElement(
                    "object",
                    {"id": "3", "count": "1", "offset": "-1"},
                    [
                        XMLParserElement("pos", {"x": "-1.5", "y": "0.25"}),
                        XMLParserElement("in1", {"component_id": "8"}),
                        XMLParserElement("inoff", {"component_id": "9"}),
                    ],
                )
            ],
        )
        expected = CompositeWriteBoolean(
            3,
            Position(-1.5, 0.25),
            0,
            1,
            None,
            Input(9, index="off"),
            {1: Input(8, index="1")},
        )
        self.assertEqual(expected, CompositeWriteBoolean.from_xml(elem))
        self.assertEqual(expected.height, 1.0)
        self.assertEqual(expected.to_xml(), elem)

    def test_max_channels(self) -> None:
        elem = XMLParserElement(
            "c",
            {"type": "41"},
            [
                XMLParserElement(
                    "object",
                    {"id": "4"},
                    [
                        XMLParserElement("pos", {"x": "2.5", "y": "1.25"}),
                        *(
                            XMLParserElement(f"in{i+1}", {"component_id": str(10 + i)})
                            for i in range(32)
                        ),
                        XMLParserElement("inc", {"component_id": "42"}),
                    ],
                )
            ],
        )
        expected = CompositeWriteBoolean(
            4,
            Position(2.5, 1.25),
            1,
            32,
            Input(42, index="c"),
            None,
            {i + 1: Input(10 + i, index=str(i + 1)) for i in range(32)},
        )
        self.assertEqual(expected, CompositeWriteBoolean.from_xml(elem))
        self.assertEqual(expected.height, 8.5)
        self.assertEqual(expected.to_xml(), elem)
