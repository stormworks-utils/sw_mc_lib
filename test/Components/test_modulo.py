import unittest

from sw_mc_lib.Components.modulo import ComponentType, Modulo
from sw_mc_lib.XMLParser import XMLParserElement

from .test_utils import BinopHelper, Input, Position


class TestModulo(BinopHelper, unittest.TestCase):
    def __init__(self, *args):
        super().__init__(ComponentType.Modulo.value, *args)

    def test_from_xml(self) -> None:
        elem: Modulo = Modulo.from_xml(self.get_empty_obj())
        expected: Modulo = Modulo(self.COMPONENT_ID, Position())
        self.assertEqual(elem, expected)
        elem = Modulo.from_xml(self.get_2_arg())
        expected.a_input = Input(self.INPUT_1, 0, "1")
        expected.b_input = Input(self.INPUT_2, 0, "2")
        self.assertEqual(elem, expected)

    def test_to_xml(self) -> None:
        elem: Modulo = Modulo(self.COMPONENT_ID, Position(), Input(self.INPUT_1))
        expected: XMLParserElement = self.get_1_arg()
        self.assertEqual(elem.to_xml(), expected)
