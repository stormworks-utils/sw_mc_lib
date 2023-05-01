from __future__ import annotations

from typing import Optional

from sw_mc_lib.Component import INNER_TO_XML_RESULT, Component
from sw_mc_lib.Input import Input
from sw_mc_lib.Position import Position
from sw_mc_lib.Types import ComponentType
from sw_mc_lib.XMLParser import XMLParserElement

DEFAULT_SCRIPT: str = """-- Tick function that will be executed every logic tick
function onTick()
\tvalue = input.getNumber(1)\t\t\t -- Read the first number from the script's composite input
\toutput.setNumber(1, value * 10)\t\t-- Write a number to the script's composite output
end

-- Draw function that will be executed when this script renders to a screen
function onDraw()
\tw = screen.getWidth()\t\t\t\t  -- Get the screen's width and height
\th = screen.getHeight()\t\t\t\t\t
\tscreen.setColor(0, 255, 0)\t\t\t -- Set draw color to green
\tscreen.drawCircleF(w / 2, h / 2, 30)   -- Draw a 30px radius circle in the center of the screen
end"""


class LuaScript(Component):
    """
    Runs a custom lua script for advanced logic and drawing to monitors.
    """

    def __init__(
        self,
        component_id: int,
        position: Position,
        script_property: str = DEFAULT_SCRIPT,
        data_input: Optional[Input] = None,
        video_input: Optional[Input] = None,
    ):
        super().__init__(ComponentType.LuaScript, component_id, position, 0.75)
        self.data_input: Optional[Input] = data_input
        self.video_input: Optional[Input] = video_input
        self.script_property: str = script_property

    @staticmethod
    def from_xml(element: XMLParserElement) -> LuaScript:
        assert element.tag == "c", f"invalid LuaScript {element}"
        assert element.attributes.get("type", "0") == str(
            ComponentType.LuaScript.value
        ), f"Not an LuaScript {element}"
        obj: XMLParserElement = element.children[0]
        component_id, position, inputs, _ = LuaScript._basic_in_parsing(obj)
        script_property: str = obj.attributes.get("script", DEFAULT_SCRIPT)
        return LuaScript(
            component_id, position, script_property, inputs.get("1"), inputs.get("2")
        )

    def _inner_to_xml(self) -> INNER_TO_XML_RESULT:
        return {"script": self.script_property}, self._pos_in_to_xml(
            self.data_input, self.video_input
        )
