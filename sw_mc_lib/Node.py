from __future__ import annotations

from typing import Optional

from .Input import Input
from .Position import Position
from .Types import NodeMode, SignalType
from .XMLElement import XMLElement
from .XMLParser import XMLParserElement


class NodePosition(XMLElement):
    """
    A Position for a node. This is distinct from :class:`sw_mc_lib.Position.Position` in that it has x, y and z, and
    that they are integers instead of floats. You probably never need to use y.
    """

    def __init__(self, x: int, z: int):
        self.x: int = x
        self.z: int = z

    @staticmethod
    def from_xml(element: XMLParserElement) -> NodePosition:
        assert element.tag == "position", f"Invalid node position {element}"
        return NodePosition(
            int(element.attributes.get("x", "0")),
            int(element.attributes.get("z", "0")),
        )

    def to_xml(self) -> XMLParserElement:
        attributes: dict[str, str] = {}
        if self.x != 0:
            attributes["x"] = str(self.x)
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
        mode: NodeMode,
        type: SignalType,
        description: str,
        input_position: Optional[NodePosition] = None,
        position: Optional[Position] = None,
        input: Optional[Input] = None,
    ):
        self.node_id: int = node_id
        self.component_id: int = component_id
        self.label: str = label
        self.mode: NodeMode = mode
        self.type: SignalType = type
        self.description: str = description
        self.input_position: Optional[NodePosition] = input_position
        self.position: Optional[Position] = position
        self.input: Optional[Input] = input

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
            NodeMode(int(node.attributes.get("mode", "0"))),
            SignalType(int(node.attributes.get("type", "0"))),
            node.attributes.get("description", ""),
            position,
        )

    def get_component_bridge_type(self) -> int:
        """
        Get the component bridge type for this node. This is the type of the mc side of the node,
        while the enum property is the id of the vehicle facing node
        :return: The component bridge type
        """
        # pylint: disable=too-many-return-statements
        match (self.mode, self.type):
            case (NodeMode.Input, SignalType.Boolean):
                return 0
            case (NodeMode.Output, SignalType.Boolean):
                return 1
            case (NodeMode.Input, SignalType.Number):
                return 2
            case (NodeMode.Output, SignalType.Number):
                return 3
            case (NodeMode.Input, SignalType.Composite):
                return 4
            case (NodeMode.Output, SignalType.Composite):
                return 5
            case (NodeMode.Input, SignalType.Video):
                return 6
            case (NodeMode.Output, SignalType.Video):
                return 7
            case (NodeMode.Input, SignalType.Audio):
                return 8
            case (NodeMode.Output, SignalType.Audio):
                return 9
            case _:
                raise ValueError(
                    f"Invalid node mode/type combination {self.mode}/{self.type}"
                )

    def add_component_bridge(self, element: XMLParserElement) -> None:
        """Add component bridge data to this node from XML (mc side of the node)"""
        assert element.tag == "c", f"Invalid node {element}"
        assert element.attributes.get("type", "0") == str(
            self.get_component_bridge_type()
        ), f"Invalid node {element}"
        node = element.children[0]
        assert node.tag == "object", f"Invalid node {element}"
        assert node.attributes.get("id", "0") == str(
            self.component_id
        ), f"Invalid node {element}"
        for child in node.children:
            if child.tag == "in1":
                self.input = Input.from_xml(child)
            elif child.tag == "pos":
                self.position = Position.from_xml(child)

    def to_component_bridge(self) -> XMLParserElement:
        """Convert this Node to a XML component bridge entity (mc side of the node)"""
        children = []
        if self.input:
            children.append(self.input.to_xml())
        if self.position:
            children.append(self.position.to_xml())
        object_ = XMLParserElement("object", {"id": str(self.component_id)}, children)
        return XMLParserElement(
            "c", {"type": str(self.get_component_bridge_type())}, [object_]
        )

    def to_component_bridge_state(self, index: int) -> XMLParserElement:
        """Convert this Node to a XML component bridge state entity (mc side of the node)"""
        children = []
        if self.input:
            self.input.index = "1"
            children.append(self.input.to_xml())
        if self.position:
            children.append(self.position.to_xml())
        return XMLParserElement(f"c{index}", {"id": str(self.component_id)}, children)

    def to_xml(self) -> XMLParserElement:
        node_attributes: dict[str, str] = {
            "label": self.label,
            "mode": str(self.mode.value),
            "type": str(self.type.value),
            "description": self.description,
        }
        node_element: XMLParserElement = XMLParserElement("node", node_attributes)
        if self.input_position:
            node_element.children.append(self.input_position.to_xml())
        return XMLParserElement(
            "n",
            {"id": str(self.node_id), "component_id": str(self.component_id)},
            [node_element],
        )

    def __hash__(self) -> int:
        return hash((self.node_id, self.component_id, self.label, self.mode, self.type))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return (
            self.node_id == other.node_id
            and self.component_id == other.component_id
            and self.label == other.label
            and self.mode == other.mode
            and self.type == other.type
            and self.description == other.description
            and self.input_position == other.input_position
            and self.position == other.position
            and self.input == other.input
        )
