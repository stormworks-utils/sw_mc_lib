from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.XMLParser import XMLParserElement


class BinopHelper:
    COMPONENT_ID: int = 123
    INPUT_1: int = 5
    INPUT_2: int = 6

    def __init__(self, component_type: int, *args):
        super().__init__(*args)
        self.component_type: int = component_type

    def embed(self, children: list[XMLParserElement]) -> XMLParserElement:
        return XMLParserElement(
            "c",
            {"type": str(self.component_type)},
            [XMLParserElement("object", {"id": str(self.COMPONENT_ID)}, children)],
        )

    def get_empty_obj(self) -> XMLParserElement:
        return self.embed([Position().to_xml()])

    def get_1_arg(self) -> XMLParserElement:
        return self.embed([Position().to_xml(), Input(self.INPUT_1, 0, "1").to_xml()])

    def get_2_arg(self) -> XMLParserElement:
        return self.embed(
            [
                Position().to_xml(),
                Input(self.INPUT_1, 0, "1").to_xml(),
                Input(self.INPUT_2, 0, "2").to_xml(),
            ]
        )
