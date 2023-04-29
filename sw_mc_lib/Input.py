from __future__ import annotations

from .XMLElement import XMLElement, XMLParserElement


class Input(XMLElement):
    def __init__(self, index: str, component_id: int, node_index: int):
        self.index: str = index
        self.component_id: int = component_id
        self.node_index: int = node_index

    @staticmethod
    def from_xml(element: XMLParserElement) -> Input:
        assert element.tag.startswith("in"), f"invalid Input {element}"
        index: str = element.tag.replace("in", "", 1)
        component_id: int = int(element.attributes.get("component_id", "0"))
        node_index: int = int(element.attributes.get("node_index", "0"))
        return Input(index, component_id, node_index)

    def to_xml(self) -> XMLParserElement:
        attributes: dict[str, str] = {"component_id": str(self.component_id)}
        if self.node_index != 0:
            attributes["node_index"] = str(self.node_index)
        return XMLParserElement(f"in{self.index}", attributes)