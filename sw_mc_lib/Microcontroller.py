from __future__ import annotations

from itertools import chain

from .Component import Component
from .Node import Node
from .XMLElement import XMLElement, XMLParserElement


class Microcontroller(XMLElement):
    """
    A Stormworks Microcontroller
    """

    def __init__(
        self,
        name: str,
        description: str,
        width: int,
        length: int,
        nodes: list[Node],
        components: list[Component],
    ):
        self.name: str = name
        self.description: str = description
        self.width: int = width
        self.length: int = length
        self.nodes: list[Node] = nodes
        self.components: list[Component] = components

    @staticmethod
    def from_xml(element: XMLParserElement) -> Microcontroller:
        assert element.tag in ("microprocessor", "microprocessor_definition")
        name: str = element.attributes.get("name", "")
        description: str = element.attributes.get("description", "")
        width: int = int(element.attributes.get("width", "0"))
        length: int = int(element.attributes.get("length", "0"))
        nodes: list[Node] = []
        nodes_elem: XMLParserElement = element.children[0]
        assert nodes_elem.tag == "nodes"
        for node in nodes_elem.children:
            nodes.append(Node.from_xml(node))
        group_elem: XMLParserElement = element.children[1]
        assert group_elem.tag == "group"
        components_elem: XMLParserElement = group_elem.children[1]
        assert components_elem.tag == "components"
        components: list[Component] = []
        for component in components_elem.children:
            components.append(Component.from_xml(component))
        return Microcontroller(name, description, width, length, nodes, components)

    def to_xml(self) -> XMLParserElement:
        nodes_elem: XMLParserElement = XMLParserElement("nodes")
        for node in self.nodes:
            nodes_elem.children.append(node.to_xml())
        group_elem: XMLParserElement = XMLParserElement("group")
        group_elem.children.append(
            XMLParserElement(
                "data", {}, [XMLParserElement("inputs"), XMLParserElement("outputs")]
            )
        )
        components_elem: XMLParserElement = XMLParserElement("components")
        for component in self.components:
            components_elem.children.append(component.to_xml())
        group_elem.children.append(components_elem)
        group_elem.children.append(XMLParserElement("components_bridge"))
        group_elem.children.append(XMLParserElement("groups"))
        components_states_elem: XMLParserElement = XMLParserElement("component_states")
        for i, component in enumerate(self.components):
            components_states_elem.children.append(component.to_state_xml(i))
        group_elem.children.append(components_states_elem)
        group_elem.children.append(XMLParserElement("component_bridge_states"))
        group_elem.children.append(XMLParserElement("group_states"))
        attributes: dict[str, str] = {
            "name": self.name,
            "description": self.description,
            "width": str(self.width),
            "length": str(self.length),
            "id_counter": str(self.id_counter),
            "id_counter_node": str(self.node_counter),
        }
        return XMLParserElement("microprocessor", attributes, [nodes_elem, group_elem])

    def add_new_component(self, component: Component) -> None:
        """
        Adds a new :class:`Component <sw_mc_lib.Component.Component>`. Sets the right `component_id`.

        :param component: The component to add, `component_id` may be any value
        :return: None
        """
        component.component_id = self.id_counter + 1
        self.components.append(component)

    def add_new_node(self, node: Node) -> None:
        """
        Adds a new :class:`Node <sw_mc_lib.Node.Node>`. Sets the right `component_id` and `node_id`.

        :param node: The Node to add
        :return: None
        """
        node.component_id = self.id_counter + 1
        node.node_id = self.node_counter + 1
        self.nodes.append(node)

    @property
    def id_counter(self) -> int:
        """
        Stormworks internal counter of what the largest component_id is.

        :return: The currently largest component_id
        """
        components = (comp.component_id for comp in self.components)
        nodes = (node.component_id for node in self.nodes)
        return max(chain(components, nodes, (0,)))

    @property
    def node_counter(self) -> int:
        """
        Stormworks internal counter of what the largest node_id is.

        :return: The currently largest node_id
        """
        nodes = (node.node_id for node in self.nodes)
        return max(chain(nodes, (0,)))
