from sw_mc_lib import Component, Microcontroller
from sw_mc_lib.Components import (
    ArithmeticFunction1In,
    ArithmeticFunction3In,
    ArithmeticFunction8In,
    BooleanFunction4In,
    BooleanFunction8In,
    CompositeWriteBoolean,
    CompositeWriteNumber,
    PropertyDropdown,
    PropertyNumber,
    PropertySlider,
    PropertyText,
    PropertyToggle,
    TooltipBoolean,
    TooltipNumber,
)
from sw_mc_lib.Types import ComponentType


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


def optimize_composite_writes(mc: Microcontroller) -> None:
    """
    Optimize composite writes by setting start_channel and channel_count.

    For example, if a composite has two inputs A and B, and both are set to the same value,
    the second write is redundant and can be removed.

    :param mc: Microcontroller to optimize
    :return: None
    """
    for component in mc.components:
        if (
            not isinstance(component, (CompositeWriteBoolean, CompositeWriteNumber))
            or component.start_channel_property == 0
        ):
            continue
        max_channel: int = max(component.channel_inputs.keys(), default=0)
        min_channel: int = min(component.channel_inputs.keys(), default=1)
        channel_count: int = max_channel - min_channel + 1
        component.channel_count_property = min(
            component.channel_count_property, channel_count
        )
        start_channel: int = component.start_channel_property
        if min_channel > 1:
            diff: int = min_channel - 1
            keys = list(component.channel_inputs.keys())
            for channel_id in keys:
                channel = component.channel_inputs[channel_id]
                component.channel_inputs[channel_id - diff] = channel
                del component.channel_inputs[channel_id]
                channel.index = str(channel_id - diff)
            component.start_channel_property = start_channel + diff


def optimize_functions(mc: Microcontroller) -> None:
    """
    Optimize the microcontroller by making function blocks as small as possible.

    :param mc: Microcontroller to optimize
    :return: None
    """
    for component in mc.components:
        if isinstance(component, ArithmeticFunction8In):
            if (
                component.a_input is None
                and component.b_input is None
                and component.c_input is None
                and component.d_input is None
                and component.w_input is None
            ):
                if component.y_input is None and component.z_input is None:
                    component.type = ComponentType.ArithmeticFunction1In
                    component.__class__ = ArithmeticFunction1In  # type: ignore
                else:
                    component.type = ComponentType.ArithmeticFunction3In
                    component.__class__ = ArithmeticFunction3In  # type: ignore
        elif isinstance(component, ArithmeticFunction3In):
            if component.y_input is None and component.z_input is None:
                component.type = ComponentType.ArithmeticFunction1In
                component.__class__ = ArithmeticFunction1In  # type: ignore
        elif isinstance(component, BooleanFunction8In):
            if (
                component.a_input is None
                and component.b_input is None
                and component.c_input is None
                and component.d_input is None
            ):
                component.type = ComponentType.BooleanFunction4In
                component.__class__ = BooleanFunction4In  # type: ignore


def optimize_tree(mc: Microcontroller) -> None:
    """
    Optimize the microcontroller by removing unused components and optimizing functions and composite writes.

    :param mc: Microcontroller to optimize
    :return: None
    """
    found: bool = True
    while found:
        found = False
        known_components: dict[Component, int] = {}
        replacements: dict[int, int] = {}
        replaced: list[int] = []
        for i, component in enumerate(mc.components):
            if component in known_components:
                replacements[component.component_id] = known_components[component]
                replaced.append(i)
                found = True
            else:
                known_components[component] = component.component_id

        if not found:
            break
        for component in mc.components:
            for input in component.inputs:
                if input.component_id in replacements:
                    input.component_id = replacements[input.component_id]

        for i in reversed(replaced):
            mc.components.pop(i)
