from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .XMLParser import XMLParserElement

from .Types import NodeMode, SignalType
from .XMLElement import XMLElement


class NodePosition(XMLElement):
    def __init__(self, x: int, y: int, z: int):
        self.x: int = x
        self.y: int = y
        self.z: int = z

    @staticmethod
    def from_xml(element: XMLParserElement) -> NodePosition:
        assert element['tag'] == 'position', f'Invalid node position {element}'
        return NodePosition(
            int(element['attributes'].get('x', '0')),
            int(element['attributes'].get('y', '0')),
            int(element['attributes'].get('z', '0')),
        )

    def to_xml(self) -> str:
        xml: str = '<position '
        if self.x != 0:
            xml += f'x="{self.x}" '
        if self.y != 0:
            xml += f'y="{self.y}" '
        if self.z != 0:
            xml += f'z="{self.z}" '
        return xml[:-1] + '/>\n'


class Node(XMLElement):
    def __init__(
        self,
        node_id: int,
        component_id: int,
        label: str,
        mode: int,
        type: int,
        description: str,
        position: Optional[NodePosition] = None
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
        assert element['tag'] == 'n', f'Invalid node {element}'
        node = element['children'][0]
        assert node['tag'] == 'node', f'Invalid node {element}'
        position: Optional[NodePosition] = None
        if node['children']:
            position = NodePosition.from_xml(node['children'][0])
        return Node(
            element['attributes'].get('id', 1),
            element['attributes'].get('component_id', 1),
            node['attributes'].get('label', ''),
            int(node['attributes'].get('mode', '0')),
            int(node['attributes'].get('type', '0')),
            node['attributes'].get('description', ''),
            position,
        )

    def to_xml(self) -> str:
        xml: str = f'<n id="{self.node_id}" component_id="{self.component_id}">\n'
        xml += f'\t<node label={self.escape_string(self.label)} mode="{self.mode.value}" '
        xml += f'type="{self.type.value}" description={self.escape_string(self.description)}'
        if self.position:
            xml += '>\n'
            xml += self.indent(self.indent(self.position.to_xml()))
            xml += '\t</node>\n'
        else:
            xml += '/>\n'
        xml += '</n>\n'
        return xml
