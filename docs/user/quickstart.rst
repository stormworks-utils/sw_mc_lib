Quickstart
==========

Parsing a file
--------------

First of all, import the :func:`parse() <sw_mc_lib.XMLParser.parse>`::

    >>> from sw_mc_lib import parse

Using the parser, you can parse XML strings into :class:`XMLParserElement <sw_mc_lib.XMLParser.XMLParserElement>` s::

    >>> element = parse('<tag attr="foo"><inner/></tag>')
    >>> element.tag
    'tag'
    >>> element.attributes
    {'attr': 'foo'}
    >>> element.children
    [XMLParserElement(tag='inner')]

These elements can be further parsed into a :class:`Microcontroller <sw_mc_lib.Microcontroller.Microcontroller>` using the :func:`from_xml() <sw_mc_lib.Microcontroller.Microcontroller.from_xml>` method::

    >>> from sw_mc_lib import Microcontroller
    >>> with open('mc.xml') as mc_file:
    ...     mc_content = mc_file.read()
    ...
    >>> mc_xml = parse(mc_content)
    >>> mc = Microcontroller.from_xml(mc_xml)

Manipulating a Microcontroller
------------------------------

To manipulate the Microcontroller, either modify existing children::

    >>> from sw_mc_lib import ComponentType, Input, Position
    >>> from sw_mc_lib.Components import AND, OR
    >>> and_component = mc.components[0]
    >>> assert and_component.type == ComponentType.AND # functionally the same as
    >>> assert isinstance(and_component, AND)
    >>> and_component.a_input = Input(and_component.component_id)
    >>> or_component = OR(0, Position())
    >>> mc.add_new_component(or_component)
    >>> or_component.a_input = Input(and_component.component_id)
    >>> and_component.b_input = Input(or_component.component_id)

Writing back to a file
----------------------

To write it to a file, first, convert the :class:`Microcontroller <sw_mc_lib.Microcontroller.Microcontroller>` into XML elements using the :func:`to_xml() <sw_mc_lib.Microcontroller.Microcontroller.to_xml>` method::

    >>> mc_xml = mc.to_xml()

And finally, format the XML elements into a string using the :func:`format() <sw_mc_lib.XMLFormatter.format>` function::

    >>> from sw_mc_lib import format
    >>> mc_content = format(mc_xml)
    >>> with open('mc.xml', 'w') as mc_file:
    ...     mc_file.write(mc_content)
    ...

