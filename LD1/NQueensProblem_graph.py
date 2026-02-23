from search import NQueensProblem, best_first_graph_search
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from collections import deque

N = 4

nq_problem = NQueensProblem(N)

# ── solve ─────────────────────────────────────────────────────────────────────
result_node = best_first_graph_search(nq_problem, lambda n: nq_problem.h(n))
solution_path = []
node = result_node
while node:
    solution_path.append(node.state)
    node = node.parent
solution_path.reverse()
print(f"Solution: {result_node.solution()}")

# ── build full state graph via BFS ────────────────────────────────────────────
def build_state_graph(problem):
    G = nx.DiGraph()
    initial = problem.initial
    G.add_node(initial, layer=0)
    queue = deque([(initial, 0)])
    visited = {initial: 0}

    while queue:
        state, depth = queue.popleft()
        for action in problem.actions(state):
            next_state = problem.result(state, action)
            if next_state not in visited:
                visited[next_state] = depth + 1
                G.add_node(next_state, layer=depth + 1)
                G.add_edge(state, next_state, action=action)
                queue.append((next_state, depth + 1))

    return G, visited

G, depths = build_state_graph(nq_problem)
print(f"States in graph: {G.number_of_nodes()}")
print(f"Edges in graph : {G.number_of_edges()}")

# ── label helpers ─────────────────────────────────────────────────────────────
def fmt_compact(state):
    """Compact tuple label, e.g. (1,3,_,_)."""
    parts = [str(r) if r != -1 else '_' for r in state]
    return '(' + ','.join(parts) + ')'

def fmt_grid(state, n):
    """Mini n×n grid string with Q and dots."""
    grid = [['.' for _ in range(n)] for _ in range(n)]
    for col, row in enumerate(state):
        if row != -1:
            grid[row][col] = 'Q'
    return '\n'.join(''.join(r) for r in grid)

# ── layout ────────────────────────────────────────────────────────────────────
pos = nx.multipartite_layout(G, subset_key='layer', align='vertical', scale=2)

# ── colours ───────────────────────────────────────────────────────────────────
solution_set = set(solution_path)

node_colors = []
for state in G.nodes():
    if state == nq_problem.initial:
        node_colors.append('#2ecc71')   # green  – initial
    elif nq_problem.goal_test(state):
        node_colors.append('#e74c3c')   # red    – goal
    elif state in solution_set:
        node_colors.append('#f39c12')   # orange – solution path
    else:
        node_colors.append('#aed6f1')   # blue   – explored

# ── draw ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(20, 13))

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=250, ax=ax)

# Background edges (grey)
nx.draw_networkx_edges(G, pos, edge_color='#bdc3c7', arrows=True,
                       arrowsize=8, width=0.6, ax=ax)

# Solution-path edges (red, highlighted)
sol_edges = list(zip(solution_path[:-1], solution_path[1:]))
nx.draw_networkx_edges(
    G, pos, edgelist=sol_edges,
    edge_color='#c0392b', width=2.5,
    arrows=True, arrowsize=14, ax=ax,
    connectionstyle='arc3,rad=0.15'
)

# Compact tuple labels for every node
compact_labels = {state: fmt_compact(state) for state in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=compact_labels,
                        font_size=6, font_family='monospace', ax=ax)

# Mini grid labels ONLY for solution-path nodes (shown above the node)
for step, state in enumerate(solution_path):
    x, y = pos[state]
    grid_text = fmt_grid(state, N)
    ax.text(x, y + 0.18, grid_text,
            ha='center', va='bottom',
            fontsize=5.5, fontfamily='monospace',
            color='#2c3e50',
            bbox=dict(boxstyle='round,pad=0.2', fc='#fdfefe', ec='none', alpha=0.8))
    # Step number
    ax.text(x, y - 0.18, f'step {step}',
            ha='center', va='top',
            fontsize=6, fontweight='bold', color='#7f8c8d')

# ── legend & title ────────────────────────────────────────────────────────────
legend_elements = [
    mpatches.Patch(color='#2ecc71', label='Initial state'),
    mpatches.Patch(color='#e74c3c', label='Goal state(s)'),
    mpatches.Patch(color='#f39c12', label='Solution path'),
    mpatches.Patch(color='#aed6f1', label='Other explored states'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
ax.set_title(
    f'{N}-Queens Problem – State Space Graph (best-first search)\n'
    f'{G.number_of_nodes()} states  |  {G.number_of_edges()} transitions  '
    f'|  solution in {len(solution_path) - 1} steps',
    fontsize=13
)
ax.axis('off')

plt.tight_layout()
plt.savefig('nqueens_graph.png', dpi=150, bbox_inches='tight')
print("Graph saved → nqueens_graph.png")
plt.show()
