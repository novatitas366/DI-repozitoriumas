# Water Jug Problem

## Problem Description

The **Water Jug Problem** is a classic AI search problem where the goal is to measure an exact amount of water using two jugs of different capacities and no measuring markings.

| Parameter | Value |
|-----------|-------|
| Jug A capacity | 4 liters |
| Jug B capacity | 3 liters |
| Initial state | A = 0L, B = 0L (both empty) |
| Goal state | A = 2L (exactly 2 liters in Jug A) |

---

## State Representation

A **state** is a tuple `(a, b)` where:
- `a` = current liters in Jug A (0 ≤ a ≤ 4)
- `b` = current liters in Jug B (0 ≤ b ≤ 3)

Total number of possible states: 5 × 4 = **20 states** (not all reachable).

---

## Available Actions

| Action | Description | Condition |
|--------|-------------|-----------|
| **Fill A** | Fill Jug A to 4L | A is not full |
| **Fill B** | Fill Jug B to 3L | B is not full |
| **Empty A** | Empty Jug A to 0L | A is not empty |
| **Empty B** | Empty Jug B to 0L | B is not empty |
| **Pour A→B** | Pour from A into B until A is empty or B is full | A > 0 and B < 3 |
| **Pour B→A** | Pour from B into A until B is empty or A is full | B > 0 and A < 4 |

### Pour Logic

When pouring, the amount transferred is:
```
pour = min(source, capacity_of_target - current_in_target)
```

For example, `Pour A→B` from state `(4, 1)`:
- `pour = min(4, 3 - 1) = min(4, 2) = 2`
- Result: `(4-2, 1+2) = (2, 3)`

---

## Search Algorithms Used

### 1. BFS (Breadth-First Search)

- Explores states level by level (by number of steps from start)
- **Guarantees the shortest solution** (fewest actions)
- Uses a FIFO queue

### 2. Best-First Search (Greedy)

- Uses a **heuristic function** to prioritize which state to explore next
- Heuristic `h(n) = |a - 2|` — how far Jug A is from the goal of 2L
- Faster in practice but does **not guarantee** the shortest path

---

## BFS Solution (Step-by-Step)

Starting from `(0, 0)`:

| Step | Action | Jug A | Jug B |
|------|--------|-------|-------|
| 0 | Start | 0L | 0L |
| 1 | Fill A | 4L | 0L |
| 2 | Pour A→B | 1L | 3L |
| 3 | Empty B | 1L | 0L |
| 4 | Pour A→B | 0L | 1L |
| 5 | Fill A | 4L | 1L |
| 6 | Pour A→B | 2L | 3L |

**Goal reached in 6 steps: A = 2L**

---

## Heuristic Function

```python
def h(self, node):
    a, b = node.state
    return abs(a - 2)
```

This is a **Manhattan-like distance** — measures how many liters away Jug A is from the goal of 2L. It is admissible (never overestimates).

---

## State-Space Graph

The program builds a full graph of all reachable states using BFS and visualizes it with **NetworkX** and **Matplotlib**.

### Node Colors

| Color | Meaning |
|-------|---------|
| Green | Initial state `(0, 0)` |
| Red | Goal state(s) where A = 2L |
| Orange | States on the BFS solution path |
| Blue | Other reachable states |

The graph is saved as `water_jug_graph.png`.

---

## Code Architecture (AIMA)

The implementation follows the **AIMA** (Artificial Intelligence: A Modern Approach) `Problem` base class:

| Method | Purpose |
|--------|---------|
| `__init__()` | Sets initial state `(0, 0)` |
| `actions(state)` | Returns all valid actions for a given state |
| `result(state, action)` | Returns the new state after an action |
| `goal_test(state)` | Returns `True` if A = 2L |
| `h(node)` | Heuristic: `abs(a - 2)` |

---

## Key Observations

- The problem has **no single path** — multiple action sequences can reach the goal.
- BFS always finds the **optimal (shortest) path**.
- The state space is small and fully explorable (at most 20 states).
- The heuristic `h(n) = |a - 2|` is simple but effective for greedy search.
