from search import EightPuzzle, breadth_first_graph_search
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from collections import deque

# ── helpers ──────────────────────────────────────────────────────────────────

def build_state_graph(puzzle, max_depth):
    """BFS from initial state; record every state up to max_depth."""
    G = nx.DiGraph()
    initial = puzzle.initial
    G.add_node(initial, layer=0)

    queue = deque([(initial, 0)])
    visited = {initial: 0}          # state -> depth

    while queue:
        state, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for action in puzzle.actions(state):
            next_state = puzzle.result(state, action)
            if next_state not in visited:
                visited[next_state] = depth + 1
                G.add_node(next_state, layer=depth + 1)
                G.add_edge(state, next_state, action=action)
                queue.append((next_state, depth + 1))

    return G, visited


def fmt(state):
    """Format a state tuple as a 3×3 grid string."""
    s = [str(x) if x != 0 else '_' for x in state]
    return f"{s[0]} {s[1]} {s[2]}\n{s[3]} {s[4]} {s[5]}\n{s[6]} {s[7]} {s[8]}"


# ── solve ────────────────────────────────────────────────────────────────────

puzzle = EightPuzzle((2, 4, 3, 1, 5, 6, 7, 8, 0))

result_node = breadth_first_graph_search(puzzle)
solution_path = []
n = result_node
while n:
    solution_path.append(n.state)
    n = n.parent
solution_path.reverse()
solution_depth = len(solution_path) - 1

print(f"Solution found in {solution_depth} moves: {result_node.solution()}")

# ── build graph ───────────────────────────────────────────────────────────────

G, depths = build_state_graph(puzzle, solution_depth)
print(f"States in graph : {G.number_of_nodes()}")
print(f"Edges in graph  : {G.number_of_edges()}")

# ── layout ────────────────────────────────────────────────────────────────────
# Group nodes by BFS depth (left = shallow, right = deep)
pos = nx.multipartite_layout(G, subset_key='layer', align='vertical', scale=2)

# ── colours ───────────────────────────────────────────────────────────────────
solution_set = set(solution_path)

node_colors = []
for node in G.nodes():
    if node == puzzle.initial:
        node_colors.append('#2ecc71')       # green  – start
    elif puzzle.goal_test(node):
        node_colors.append('#e74c3c')       # red    – goal
    elif node in solution_set:
        node_colors.append('#f39c12')       # orange – on solution path
    else:
        node_colors.append('#aed6f1')       # blue   – explored

# ── draw ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(max(18, solution_depth * 3), 14))

# All nodes and background edges
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=180, ax=ax)
nx.draw_networkx_edges(G, pos, edge_color='#d5d8dc', arrows=False, width=0.4, ax=ax)

# Solution-path edges (red, with arrows)
sol_edges = list(zip(solution_path[:-1], solution_path[1:]))
nx.draw_networkx_edges(
    G, pos, edgelist=sol_edges,
    edge_color='#c0392b', width=2.5,
    arrows=True, arrowsize=12, ax=ax,
    connectionstyle='arc3,rad=0.1'
)

# Labels only for solution-path nodes (tiny 3×3 grid)
labels = {state: fmt(state) for state in solution_path}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=5, font_family='monospace', ax=ax)

# Step numbers along the solution path
for step, state in enumerate(solution_path):
    x, y = pos[state]
    ax.text(x, y + 0.10, str(step), ha='center', va='bottom', fontsize=6,
            fontweight='bold', color='#2c3e50')

# ── legend & title ────────────────────────────────────────────────────────────
legend_elements = [
    mpatches.Patch(color='#2ecc71', label='Initial state'),
    mpatches.Patch(color='#e74c3c', label='Goal state'),
    mpatches.Patch(color='#f39c12', label='Solution path'),
    mpatches.Patch(color='#aed6f1', label='Other explored states'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
ax.set_title(
    f'Eight Puzzle – BFS state-space graph\n'
    f'Initial: {puzzle.initial}   Goal: {puzzle.goal}\n'
    f'{G.number_of_nodes()} states explored   |   solution in {solution_depth} moves',
    fontsize=13
)
ax.axis('off')

plt.tight_layout()
plt.savefig('eight_puzzle_graph.png', dpi=150, bbox_inches='tight')
print("Graph saved → eight_puzzle_graph.png")
plt.show()
