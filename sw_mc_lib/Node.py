from __future__ import annotations

from typing import Optional

from .Types import NodeMode, SignalType
from .XMLElement import XMLElement
from .XMLParser import XMLParserElement


class NodePosition(XMLElement):
    """
    A Position for a node. This is distinct from :class:`sw_mc_lib.Position.Position` in that it has x, y and z, and
    that they are integers instead of floats. You probably never need to use y.
    """

    def __init__(self, x: int, y: int, z: int):
        self.x: int = x
        self.y: int = y
        self.z: int = z

    @staticmethod
    def from_xml(element: XMLParserElement) -> NodePosition:
        assert element.tag == "position", f"Invalid node position {element}"
        return NodePosition(
            int(element.attributes.get("x", "0")),
            int(element.attributes.get("y", "0")),
            int(element.attributes.get("z", "0")),
        )

    def to_xml(self) -> XMLParserElement:
        attributes: dict[str, str] = {}
        if self.x != 0:
            attributes["x"] = str(self.x)
        if self.y != 0:
            attributes["y"] = str(self.y)
        if self.z != 0:
            attributes["z"] = str(self.z)
        return XMLParserElement("position", attributes)


class Node(XMLElement):
    """
    A Microcontroller node. Interface between Microcontroller and the rest of the Vehicle.
    """

    def __init__(
        self,
        node_id: int,
        component_id: int,
        label: str,
        mode: int,
        type: int,
        description: str,
        position: Optional[NodePosition] = None,
    ):
        self.node_id: int = node_id
        self.component_id: int = component_id
        self.label: str = label
        self.mode: NodeMode = NodeMode(mode)
        self.type: SignalType = SignalType(type)
        self.description: str = description
        self.position: Optional[NodePosition] = position

    @staticmethod
    def from_xml(element: XMLParserElement) -> Node:
        assert element.tag == "n", f"Invalid node {element}"
        node = element.children[0]
        assert node.tag == "node", f"Invalid node {element}"
        position: Optional[NodePosition] = None
        if node.children:
            position = NodePosition.from_xml(node.children[0])
        return Node(
            int(element.attributes.get("id", "1")),
            int(element.attributes.get("component_id", "1")),
            node.attributes.get("label", ""),
            int(node.attributes.get("mode", "0")),
            int(node.attributes.get("type", "0")),
            node.attributes.get("description", ""),
            position,
        )

    def to_xml(self) -> XMLParserElement:
        node_attributes: dict[str, str] = {
            "label": self.label,
            "mode": str(self.mode.value),
            "type": str(self.type.value),
            "description": self.description,
        }
        node_element: XMLParserElement = XMLParserElement("node", node_attributes)
        if self.position:
            node_element.children.append(self.position.to_xml())
        return XMLParserElement(
            "n",
            {"id": str(self.node_id), "component_id": str(self.component_id)},
            [node_element],
        )
