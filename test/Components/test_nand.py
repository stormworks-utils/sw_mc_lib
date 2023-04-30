import unittest

from sw_mc_lib.Components.NAND import NAND, ComponentType
from sw_mc_lib.XMLParser import XMLParser, XMLParserElement

from .test_utils import BinopHelper, Input, Position


class TestNAND(BinopHelper, unittest.TestCase):
    def __init__(self, *args):
        super().__init__(ComponentType.NAND.value, *args)

    @staticmethod
    def parse(xml: str) -> XMLParserElement:
        return XMLParser(xml).parse()

    def test_from_xml(self) -> None:
        elem: NAND = NAND.from_xml(self.get_empty_obj())
        expected: NAND = NAND(self.COMPONENT_ID, Position.empty_pos())
        self.assertEqual(elem, expected)
        elem = NAND.from_xml(self.get_2_arg())
        expected.a_input = Input(self.INPUT_1, 0, "1")
        expected.b_input = Input(self.INPUT_2, 0, "2")
        self.assertEqual(elem, expected)

    def test_to_xml(self) -> None:
        elem: NAND = NAND(self.COMPONENT_ID, Position.empty_pos(), Input(self.INPUT_1))
        expected: XMLParserElement = self.get_1_arg()
        self.assertEqual(elem.to_xml(), expected)
