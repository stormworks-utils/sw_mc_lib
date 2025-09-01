from sw_mc_lib import Microcontroller
from sw_mc_lib.Components import (
    PropertyDropdown,
    PropertyNumber,
    PropertySlider,
    PropertyText,
    PropertyToggle,
    TooltipBoolean,
    TooltipNumber,
)


def remove_unused(mc: Microcontroller) -> None:
    """
    Remove all components that do not contribute to any output or global variable.

    Also checks for components that are only cyclically connected and removes them.
    :param mc: Microcontroller to optimize
    :return: None
    """
    components_by_id = {}
    to_remove: set[int] = set()
    for component in mc.components:
        if isinstance(component, (TooltipBoolean, TooltipNumber)):
            # Tooltips are outputs out of the mc of their own
            if component.display_number_input:
                to_remove.add(component.display_number_input.component_id)
        elif not isinstance(
            component,
            (
                PropertyNumber,
                PropertyDropdown,
                PropertySlider,
                PropertyText,
                PropertyToggle,
            ),
        ):
            # Properties can be accessed without any connection in lua
            components_by_id[component.component_id] = component

    for node in mc.nodes:
        if node.input:
            to_remove.add(node.input.component_id)

    while to_remove:
        current = to_remove.pop()
        if current not in components_by_id:
            continue
        current_component = components_by_id.pop(current)
        for input in current_component.inputs:
            to_remove.add(input.component_id)

    for component in components_by_id.values():
        mc.components.remove(component)
