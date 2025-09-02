from typing import TypedDict

from sw_mc_lib import Component, Microcontroller
from sw_mc_lib import Node as MCNode
from sw_mc_lib import Position

NodeID = int


class Node(TypedDict):
    """A node in the graph for layout purposes."""

    id: NodeID
    inputs: list[NodeID]
    width: float
    height: float


def _layout_nodes_variable_heights(
    nodes: list[Node],
    width: float = 1.0,
    spacing: float = 0.25,
) -> dict[NodeID, Position]:
    """
    A practical implementation of the Sugiyama-style layered layout for nodes with variable heights.

    - Nodes are assumed to be horizontal boxes: inputs on left, outputs on right.
    - `nodes` is a list of Node typed dicts where `inputs` are NodeIDs pointing to upstream nodes.
    - Returns a mapping NodeID -> Position.

    Algorithm outline:
    1. Build directed graph edges input -> node.
    2. Condense strongly-connected components (Tarjan) to handle cycles.
    3. Assign layers using longest-path layering on the component DAG (sources at layer 0).
    4. Reduce crossings by repeated barycenter ordering between adjacent layers.
    5. Assign x coordinates by layer index and y coordinates by stacking nodes in each layer considering node heights and spacing.

    This is intended as a robust, readable implementation rather than the most optimized.
    """
    # pylint: disable=too-many-locals,too-many-statements,too-many-branches

    # --- Helpers ---
    node_map: dict[NodeID, Node] = {n["id"]: n for n in nodes}

    # Build adjacency: edges input -> node
    adj: dict[NodeID, list[NodeID]] = {nid: [] for nid in node_map}
    rev_adj: dict[NodeID, list[NodeID]] = {nid: [] for nid in node_map}
    for n in nodes:
        for src in n["inputs"]:
            if src not in node_map:
                # ignore missing references
                continue
            adj[src].append(n["id"])  # src -> n
            rev_adj[n["id"]].append(src)

    # --- Break cycles by removing edges (heuristic) ---
    # Instead of condensing SCCs, iteratively find a cycle and remove a single edge from that
    # cycle. Prefer removing the edge whose *source* node has the largest outbound degree
    # (heuristic: removing from hub-like nodes minimizes loss of connectivity overall).
    # We operate on a copy of `adj` so the original adjacency is still available for later use
    # (for example to draw or inspect removed edges).
    adj_copy: dict[NodeID, list[NodeID]] = {nid: list(adj[nid]) for nid in adj}

    def _find_cycle_in_copy() -> list[NodeID] | None:
        visited: set[NodeID] = set()
        stack: list[NodeID] = []
        onstack: set[NodeID] = set()

        def dfs(u: NodeID) -> list[NodeID] | None:
            visited.add(u)
            stack.append(u)
            onstack.add(u)
            for v in adj_copy.get(u, []):
                if v not in visited:
                    res = dfs(v)
                    if res:
                        return res
                elif v in onstack:
                    # found a cycle: return the cycle nodes (v...u, and back to v)
                    try:
                        idx = stack.index(v)
                        return stack[idx:] + [v]
                    except ValueError:
                        return [v, u, v]
            stack.pop()
            onstack.remove(u)
            return None

        for n in node_map:
            if n not in visited:
                c = dfs(n)
                if c:
                    return c
        return None

    # Greedily remove edges until the graph is acyclic
    while True:
        cycle = _find_cycle_in_copy()
        if not cycle:
            break
        # cycle is a list like [n1, n2, ..., nk, n1]
        # choose an edge (s->t) in that cycle whose source s has the largest out-degree
        best_edge: tuple[NodeID, NodeID] | None = None
        best_outdeg = -1
        for i in range(len(cycle) - 1):
            s = cycle[i]
            t = cycle[i + 1]
            outdeg = len(adj_copy.get(s, []))
            if outdeg > best_outdeg:
                best_outdeg = outdeg
                best_edge = (s, t)
        if best_edge:
            s, t = best_edge
            if t in adj_copy.get(s, []):
                adj_copy[s].remove(t)

    # Now adj_copy is a DAG (acyclic). Build reverse adjacency for barycenter and layering.
    dag_adj: dict[NodeID, list[NodeID]] = adj_copy
    dag_rev: dict[NodeID, list[NodeID]] = {nid: [] for nid in node_map}
    for u, outs in dag_adj.items():
        for v in outs:
            dag_rev[v].append(u)

    # --- Longest-path layering on component DAG ---
    # topological order via Kahn
    indeg = {i: 0 for i in dag_adj}
    for u, outs in dag_adj.items():
        for v in outs:
            indeg[v] += 1
    queue = [u for u, d in indeg.items() if d == 0]
    topo: list[int] = []
    qidx = 0
    while qidx < len(queue):
        u = queue[qidx]
        qidx += 1
        topo.append(u)
        for v in dag_adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    if len(topo) != len(dag_adj):
        # Shouldn't happen after SCC condensation, but guard just in case.
        topo = list(dag_adj.keys())

    comp_layer: dict[int, int] = {i: 0 for i in dag_adj}
    for u in reversed(topo):
        for v in dag_rev[u]:
            comp_layer[v] = min(comp_layer[v], comp_layer[u] - 1)

    min_layer = min(comp_layer.values(), default=0)

    for u in topo:
        if dag_rev[u]:
            comp_layer[u] = max(comp_layer[v] + 1 for v in dag_rev[u])

    # Map nodes to layers
    layer_of: dict[NodeID, int] = {nid: comp_layer[nid] - min_layer for nid in node_map}

    # Build layers list (ordered)
    max_layer = max(layer_of.values()) if layer_of else 0
    layers: dict[int, list[NodeID]] = {i: [] for i in range(max_layer + 1)}
    for nid in node_map:
        layers[layer_of[nid]].append(nid)

    # Initial ordering: sort by number of inputs (heuristic) for stability
    for layer in layers:
        layers[layer].sort(key=lambda nid: (len(rev_adj[nid]), node_map[nid]["id"]))

    # --- Crossing reduction: barycenter heuristic ---
    def barycenter_order(layer_index: int, use_prev: bool) -> None:
        """Reorder nodes in layer `layer_index` using barycenters to adjacent layer.
        If use_prev is True, compute barycenters using nodes in previous layer (parents).
        Otherwise use next layer (children).
        """
        nodes_in_layer = layers[layer_index]
        if not nodes_in_layer:
            return
        neighbor_layer_index = layer_index - 1 if use_prev else layer_index + 1
        if neighbor_layer_index < 0 or neighbor_layer_index > max_layer:
            return
        neighbor_order = {nid: i for i, nid in enumerate(layers[neighbor_layer_index])}
        bary: list[tuple[float, int, NodeID]] = []  # (barycenter, original_index, nid)
        for i, nid in enumerate(nodes_in_layer):
            neighbors = rev_adj[nid] if use_prev else adj[nid]
            idxs = []
            for n in neighbors:
                if n in neighbor_order:
                    relative: int
                    if use_prev:
                        node = node_map[nid]
                        relative = node["inputs"].index(n)
                    else:
                        node = node_map[n]
                        relative = -node["inputs"].index(nid)
                    idxs.append(
                        neighbor_order[n] + (relative * 0.02)
                    )  # slight offset for input order
            if idxs:
                b = sum(idxs) / len(idxs)
                bary.append((b, i, nid))
            else:
                bary.append((float("inf"), i, nid))
        bary.sort(key=lambda t: (t[0], t[1]))
        layers[layer_index] = [t[2] for t in bary]

    # iterate barycenter passes
    passes = 24
    for _ in range(passes):
        # forward pass (left to right): use previous layer parents
        for li in range(1, max_layer + 1):
            barycenter_order(li, use_prev=True)
        # backward pass (right to left): use next layer children
        for li in range(max_layer - 1, -1, -1):
            barycenter_order(li, use_prev=False)

    # --- Coordinate assignment ---
    positions: dict[NodeID, Position] = {}

    x_offset = (max_layer * (width + spacing)) / 8 * 4
    # x per layer
    x_of_layer = {i: i * (width + spacing) - x_offset for i in range(max_layer + 1)}

    # For each layer, compute y positions by stacking nodes with spacing, centered at y=0
    for li in range(max_layer + 1):
        order = layers[li]
        if not order:
            continue
        heights = [node_map[nid]["height"] for nid in order]
        total_h = (sum(heights) + spacing * (len(order) - 1)) * 4 // 4
        start_y = -total_h / 2.0
        y = start_y
        for nid, h in zip(order, heights):
            positions[nid] = Position(x_of_layer[li], y)
            y += h + spacing

    return positions


def layout_mc(mc: Microcontroller) -> None:
    """
    Layout the components and nodes of a Microcontroller in a Sugiyama-style layered layout.
    Modifies the `position` attribute of each component and node in place.
    """
    all_components: dict[NodeID, MCNode | Component] = {}
    nodes: list[Node] = []
    for n in mc.nodes:
        node_inputs: list[NodeID] = []
        if n.input:
            node_inputs.append(n.input.component_id)
        nodes.append(
            {
                "id": n.component_id,
                "inputs": node_inputs,
                "width": 1.0,
                "height": 0.5,
            }
        )
        all_components[n.component_id] = n
    for component in mc.components:
        nodes.append(
            {
                "id": component.component_id,
                "inputs": [input.component_id for input in component.inputs],
                "width": 1.0,
                "height": component.height,
            }
        )
        if component.component_id in nodes[-1]["inputs"]:
            # There is no use of self references for layout purposes.
            nodes[-1]["inputs"].remove(component.component_id)
        all_components[component.component_id] = component
    positions = _layout_nodes_variable_heights(nodes, width=1.0, spacing=0.25)
    for nid, pos in positions.items():
        all_components[nid].position = pos
