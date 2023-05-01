import unittest

from sw_mc_lib.Components.AND import AND, ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

from .test_utils import BinopHelper, Input, Position


class TestAND(BinopHelper, unittest.TestCase):
    def __init__(self, *args):
        super().__init__(ComponentType.AND.value, *args)

    def test_from_xml(self) -> None:
        elem: AND = AND.from_xml(self.get_empty_obj())
        expected: AND = AND(self.COMPONENT_ID, Position())
        self.assertEqual(elem, expected)
        elem = AND.from_xml(self.get_2_arg())
        expected.a_input = Input(self.INPUT_1, 0, "1")
        expected.b_input = Input(self.INPUT_2, 0, "2")
        self.assertEqual(elem, expected)

    def test_to_xml(self) -> None:
        elem: AND = AND(self.COMPONENT_ID, Position(), Input(self.INPUT_1))
        expected: XMLParserElement = self.get_1_arg()
        self.assertEqual(elem.to_xml(), expected)
