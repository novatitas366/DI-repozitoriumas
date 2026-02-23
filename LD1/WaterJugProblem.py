# =============================================================================
# AI PROMPT (GitHub Copilot / Claude):
#
# "Using the AIMA search.py architecture (Problem base class with initial,
#  goal, actions(), result(), goal_test(), h() methods), implement the classic
#  Water Jug Problem:
#   - Jug A holds up to 4 liters, Jug B holds up to 3 liters.
#   - Start: both jugs empty (0, 0).
#   - Goal: get exactly 2 liters in Jug A.
#   - Actions: Fill A, Fill B, Empty A, Empty B, Pour A->B, Pour B->A.
#  Solve it with BFS, DFS, and best-first search.
#  Print the step-by-step solution and draw a matplotlib visualisation
#  of the state-space graph using networkx."
# =============================================================================

from search import Problem, breadth_first_graph_search, depth_first_graph_search, best_first_graph_search
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from collections import deque


class WaterJugProblem(Problem):
    """
    Water Jug Problem – AIMA architecture.

    State: (a, b)  where  a = liters in Jug A,  b = liters in Jug B
    Initial state : (0, 0)   – both jugs empty
    Goal state    : a == 2   – exactly 2 liters in Jug A

    Jug capacities:
      Jug A – 4 liters
      Jug B – 3 liters

    Available actions:
      'Fill A'    – fill Jug A to capacity
      'Fill B'    – fill Jug B to capacity
      'Empty A'   – empty Jug A completely
      'Empty B'   – empty Jug B completely
      'Pour A->B' – pour from A into B (until A empty or B full)
      'Pour B->A' – pour from B into A (until B empty or A full)
    """

    CAP_A = 4   # Jug A capacity (liters)
    CAP_B = 3   # Jug B capacity (liters)

    def __init__(self):
        super().__init__(initial=(0, 0))  # goal checked dynamically

    def actions(self, state):
        """Return all valid actions in the current state."""
        a, b = state
        possible = []
        if a < self.CAP_A:            possible.append('Fill A')
        if b < self.CAP_B:            possible.append('Fill B')
        if a > 0:                     possible.append('Empty A')
        if b > 0:                     possible.append('Empty B')
        if a > 0 and b < self.CAP_B: possible.append('Pour A->B')
        if b > 0 and a < self.CAP_A: possible.append('Pour B->A')
        return possible

    def result(self, state, action):
        """Return the new state after performing action."""
        a, b = state
        if action == 'Fill A':
            return (self.CAP_A, b)
        elif action == 'Fill B':
            return (a, self.CAP_B)
        elif action == 'Empty A':
            return (0, b)
        elif action == 'Empty B':
            return (a, 0)
        elif action == 'Pour A->B':
            pour = min(a, self.CAP_B - b)
            return (a - pour, b + pour)
        elif action == 'Pour B->A':
            pour = min(b, self.CAP_A - a)
            return (a + pour, b - pour)

    def goal_test(self, state):
        """Goal: exactly 2 liters in Jug A."""
        return state[0] == 2

    def h(self, node):
        """
        Heuristic: Manhattan-like distance to goal.
        How far is Jug A from 2 liters?
        """
        a, b = node.state
        return abs(a - 2)


# ── Helper: build full state graph ────────────────────────────────────────────

def build_state_graph(problem):
    """BFS over all reachable states; return a networkx DiGraph."""
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
                G.add_edge(state, next_state, label=action)
                queue.append((next_state, depth + 1))

    return G


# ── Solve ──────────────────────────────────────────────────────────────────────

problem = WaterJugProblem()

print("=" * 50)
print("  Water Jug Problem")
print(f"  Jug A capacity : {problem.CAP_A} L")
print(f"  Jug B capacity : {problem.CAP_B} L")
print(f"  Initial state  : {problem.initial}  (A=0L, B=0L)")
print(f"  Goal           : A == 2 L")
print("=" * 50)

# BFS – guarantees fewest steps
bfs_node = breadth_first_graph_search(problem)
bfs_solution = bfs_node.solution()
print(f"\nBFS solution  ({len(bfs_solution)} steps): {bfs_solution}")

# Best-first (greedy) – uses heuristic h(n)
bef_node = best_first_graph_search(problem, lambda n: problem.h(n))
bef_solution = bef_node.solution()
print(f"Best-first    ({len(bef_solution)} steps): {bef_solution}")

# Step-by-step trace (BFS solution)
print("\nStep-by-step (BFS):")
state = problem.initial
print(f"  Start : A={state[0]}L, B={state[1]}L")
for action in bfs_solution:
    state = problem.result(state, action)
    print(f"  {action:<12}: A={state[0]}L, B={state[1]}L")

# ── Build & draw state-space graph ────────────────────────────────────────────

G = build_state_graph(problem)
print(f"\nState-space graph: {G.number_of_nodes()} states, {G.number_of_edges()} transitions")

# Recover solution path nodes
solution_path = []
node = bfs_node
while node:
    solution_path.append(node.state)
    node = node.parent
solution_path.reverse()
solution_set = set(solution_path)

# Layout by BFS depth layer
pos = nx.multipartite_layout(G, subset_key='layer', align='vertical', scale=2)

# Node colours
node_colors = []
for s in G.nodes():
    if s == problem.initial:
        node_colors.append('#2ecc71')   # green  – initial
    elif problem.goal_test(s):
        node_colors.append('#e74c3c')   # red    – goal
    elif s in solution_set:
        node_colors.append('#f39c12')   # orange – solution path
    else:
        node_colors.append('#aed6f1')   # blue   – explored

fig, ax = plt.subplots(figsize=(16, 10))

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900, ax=ax)

# All edges (grey)
nx.draw_networkx_edges(G, pos, edge_color='#bdc3c7', arrows=True,
                       arrowsize=12, width=0.7, ax=ax)

# Solution-path edges (red)
sol_edges = list(zip(solution_path[:-1], solution_path[1:]))
nx.draw_networkx_edges(
    G, pos, edgelist=sol_edges,
    edge_color='#c0392b', width=3,
    arrows=True, arrowsize=18, ax=ax,
    connectionstyle='arc3,rad=0.15'
)

# Node labels: (A, B) liters
labels = {s: f"A={s[0]}L\nB={s[1]}L" for s in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

# Edge action labels on solution path
edge_labels = {(u, v): G[u][v]['label'] for u, v in sol_edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                             font_size=7, font_color='#c0392b', ax=ax)

# Step numbers on solution path
for step, s in enumerate(solution_path):
    x, y = pos[s]
    ax.text(x, y + 0.18, f"step {step}",
            ha='center', va='bottom', fontsize=7,
            fontweight='bold', color='#2c3e50')

legend_elements = [
    mpatches.Patch(color='#2ecc71', label='Initial state (0L, 0L)'),
    mpatches.Patch(color='#e74c3c', label='Goal state (A = 2L)'),
    mpatches.Patch(color='#f39c12', label='Solution path (BFS)'),
    mpatches.Patch(color='#aed6f1', label='Other reachable states'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
ax.set_title(
    f"Water Jug Problem – State-Space Graph (BFS)\n"
    f"Jug A: {problem.CAP_A}L  |  Jug B: {problem.CAP_B}L  |  "
    f"Goal: A=2L  |  BFS solution: {len(bfs_solution)} steps\n"
    f"{G.number_of_nodes()} states  |  {G.number_of_edges()} transitions",
    fontsize=13
)
ax.axis('off')
plt.tight_layout()
plt.savefig('water_jug_graph.png', dpi=150, bbox_inches='tight')
print("Graph saved → water_jug_graph.png")
plt.show()
