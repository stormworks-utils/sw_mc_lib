import unittest

from sw_mc_lib.Components.abs import Abs, ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .test_utils import BinopHelper, Input, Position


class TestAbs(BinopHelper, unittest.TestCase):
    def __init__(self, *args):
        super().__init__(ComponentType.Abs.value, *args)

    def test_from_xml(self) -> None:
        elem: Abs = Abs.from_xml(self.get_empty_obj())
        expected: Abs = Abs(self.COMPONENT_ID, Position())
        self.assertEqual(elem, expected)
        elem = Abs.from_xml(self.get_2_arg())
        expected.number_input = Input(self.INPUT_1, 0, "1")
        self.assertEqual(elem, expected)

    def test_to_xml(self) -> None:
        elem: Abs = Abs(self.COMPONENT_ID, Position(), Input(self.INPUT_1))
        expected: XMLParserElement = self.get_1_arg()
        self.assertEqual(elem.to_xml(), expected)
