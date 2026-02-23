# BFS (Breadth-First Search) — pilnas paaiškinimas

## Kas tai?

**BFS (Plotis-pirmiau paieška)** — paieškos algoritmas, kuris tyrinėja grafą / medį **sluoksniais**:
pirmiausia visi 1 žingsnio atstumu nuo pradžios, po to visi 2 žingsnių atstumu ir t.t.

Garantuoja **trumpiausią kelią** (pagal žingsnių skaičių).

---

## Pagrindinės duomenų struktūros

| Struktūra | Tipas | Paskirtis |
|---|---|---|
| `frontier` | `deque` (FIFO eilė) | Mazgai laukiantys nagrinėjimo |
| `explored` | `set` | Jau aplankytos būsenos |
| `node` | `Node` objektas | Dabartinis mazgas |

---

## Algoritmo žingsniai (pseudokodas)

```
1. Sukurk pradinį mazgą iš problem.initial
2. Jei pradžia = tikslas → grąžink iš karto
3. Įdėk pradinį mazgą į frontier (eilę)
4. explored = tuščia aibė

5. KOL frontier nėra tuščia:
   a. Išimk mazgą iš KAIRĖS eilės (seniausias)
   b. Pridėk jo būseną į explored
   c. Kiekvienam vaiko mazgui (expand):
      - Jei vaikas ne explored ir ne frontier:
          - Jei vaikas = tikslas → GRĄŽINK
          - Kitaip → įdėk į DEŠINĘ eilės (append)

6. Grąžink None (sprendimo nėra)
```

---

## Kodas su komentarais (`search.py`)

```python
def breadth_first_graph_search(problem, step_limits=-1):
    node = Node(problem.initial)          # pradinis mazgas
    if problem.goal_test(node.state):     # ar iš karto tikslas?
        return node

    frontier = deque([node])              # FIFO eilė — pradedame su pradiniu mazgu
    explored = set()                      # aplankytų būsenų aibė
    step_num = 0

    while frontier:                       # kol yra ką nagrinėti
        step_num += 1
        node = frontier.popleft()         # ← imame iš kairės (seniausias mazgas)

        if step_limits > 0 and step_num >= step_limits:
            return node                   # debug sustojimas

        explored.add(node.state)          # žymime kaip aplankytą

        for child in node.expand(problem):           # visi galimi vaikai
            if child.state not in explored \
               and child not in frontier:             # dar nematytas?
                if problem.goal_test(child.state):
                    return child                      # ← TIKSLAS RASTAS
                frontier.append(child)               # → dedame į dešinę

    return None                           # sprendimo nėra
```

---

## BFS savybės

| Savybė | Reikšmė | Paaiškinimas |
|---|---|---|
| **Pilnumas** | ✅ Taip | Visada ras sprendimą jei jis egzistuoja (baigtiniame grafe) |
| **Optimalumas** | ✅ Taip | Randa trumpiausią kelią (minimalus žingsnių sk.) |
| **Laiko sudėtingumas** | O(b^d) | b = šakojimosi faktorius, d = sprendimo gylis |
| **Erdvės sudėtingumas** | O(b^d) | Saugo visą frontier atmintyje — didžiausia silpnybė |

**Eight Puzzle atveju:** b ≈ 3 (vid. 3 galimi veiksmai), todėl gali išaugti labai greitai.

---

## Kodėl FIFO (ne LIFO)?

- **FIFO (deque)** → BFS → nagrinėja sluoksniais → **optimalu**
- **LIFO (stack)** → DFS → eina gilyn → **neoptimalu**, gali užstrigti

```
FIFO:  [A] → [B, C] → [C, D, E] → [D, E, F, G]
        d=0     d=1        d=1          d=2
        ↑ visada nagrinėjame sekančią eilę tik išbaigę dabartinę
```

---

## Eight Puzzle — BFS schema

Pradinė būsena: `(2, 4, 3, 1, 5, 6, 7, 8, 0)` → BFS randa sprendimą **per 8 žingsnius**.

### Būsenų lentelė

| Žingsnis | Veiksmas | state kortežas | `node.depth` | `node.path_cost` |
|---|---|---|---|---|
| 0 | — (pradžia) | `(2,4,3, 1,5,6, 7,8,0)` | 0 | 0 |
| 1 | `UP` | `(2,4,3, 1,5,0, 7,8,6)` | 1 | 1 |
| 2 | `LEFT` | `(2,4,3, 1,0,5, 7,8,6)` | 2 | 2 |
| 3 | `UP` | `(2,0,3, 1,4,5, 7,8,6)` | 3 | 3 |
| 4 | `LEFT` | `(0,2,3, 1,4,5, 7,8,6)` | 4 | 4 |
| 5 | `DOWN` | `(1,2,3, 0,4,5, 7,8,6)` | 5 | 5 |
| 6 | `RIGHT` | `(1,2,3, 4,0,5, 7,8,6)` | 6 | 6 |
| 7 | `RIGHT` | `(1,2,3, 4,5,0, 7,8,6)` | 7 | 7 |
| 8 | `DOWN` | `(1,2,3, 4,5,6, 7,8,0)` | 8 | 8 |

---

### Vizualinė schema

```
┌─────────────┐
│  PRADŽIA    │  state = (2,4,3,1,5,6,7,8,0)
│  ┌─┬─┬─┐   │  depth = 0
│  │2│4│3│   │  path_cost = 0
│  ├─┼─┼─┤   │  frontier = [(pradžia)]
│  │1│5│6│   │  explored = {}
│  ├─┼─┼─┤   │
│  │7│8│_│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: UP (tuščia vieta juda aukštyn)
       │ frontier.popleft() → expand() → frontier.append(child)
       ▼
┌─────────────┐
│  Žingsnis 1 │  state = (2,4,3,1,5,0,7,8,6)
│  ┌─┬─┬─┐   │  depth = 1
│  │2│4│3│   │  path_cost = 1
│  ├─┼─┼─┤   │  action = 'UP'
│  │1│5│_│   │  explored = {(2,4,3,1,5,6,7,8,0)}
│  ├─┼─┼─┤   │
│  │7│8│6│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: LEFT
       ▼
┌─────────────┐
│  Žingsnis 2 │  state = (2,4,3,1,0,5,7,8,6)
│  ┌─┬─┬─┐   │  depth = 2
│  │2│4│3│   │  path_cost = 2
│  ├─┼─┼─┤   │  action = 'LEFT'
│  │1│_│5│   │
│  ├─┼─┼─┤   │
│  │7│8│6│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: UP
       ▼
┌─────────────┐
│  Žingsnis 3 │  state = (2,0,3,1,4,5,7,8,6)
│  ┌─┬─┬─┐   │  depth = 3
│  │2│_│3│   │  path_cost = 3
│  ├─┼─┼─┤   │  action = 'UP'
│  │1│4│5│   │
│  ├─┼─┼─┤   │
│  │7│8│6│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: LEFT
       ▼
┌─────────────┐
│  Žingsnis 4 │  state = (0,2,3,1,4,5,7,8,6)
│  ┌─┬─┬─┐   │  depth = 4
│  │_│2│3│   │  path_cost = 4
│  ├─┼─┼─┤   │  action = 'LEFT'
│  │1│4│5│   │
│  ├─┼─┼─┤   │
│  │7│8│6│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: DOWN
       ▼
┌─────────────┐
│  Žingsnis 5 │  state = (1,2,3,0,4,5,7,8,6)
│  ┌─┬─┬─┐   │  depth = 5
│  │1│2│3│   │  path_cost = 5
│  ├─┼─┼─┤   │  action = 'DOWN'
│  │_│4│5│   │  ← pirmoji eilutė jau teisinga!
│  ├─┼─┼─┤   │
│  │7│8│6│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: RIGHT
       ▼
┌─────────────┐
│  Žingsnis 6 │  state = (1,2,3,4,0,5,7,8,6)
│  ┌─┬─┬─┐   │  depth = 6
│  │1│2│3│   │  path_cost = 6
│  ├─┼─┼─┤   │  action = 'RIGHT'
│  │4│_│5│   │
│  ├─┼─┼─┤   │
│  │7│8│6│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: RIGHT
       ▼
┌─────────────┐
│  Žingsnis 7 │  state = (1,2,3,4,5,0,7,8,6)
│  ┌─┬─┬─┐   │  depth = 7
│  │1│2│3│   │  path_cost = 7
│  ├─┼─┼─┤   │  action = 'RIGHT'
│  │4│5│_│   │
│  ├─┼─┼─┤   │
│  │7│8│6│   │
│  └─┴─┴─┘   │
└──────┬──────┘
       │ veiksmas: DOWN
       ▼
┌─────────────┐
│  TIKSLAS    │  state = (1,2,3,4,5,6,7,8,0)
│  ┌─┬─┬─┐   │  depth = 8
│  │1│2│3│   │  path_cost = 8
│  ├─┼─┼─┤   │  goal_test() → TRUE ✅
│  │4│5│6│   │  solution() = ['UP','LEFT','UP','LEFT',
│  ├─┼─┼─┤   │               'DOWN','RIGHT','RIGHT','DOWN']
│  │7│8│_│   │
│  └─┴─┴─┘   │
└─────────────┘
```

---

## Kaip `explored` ir `frontier` apsaugo nuo ciklų

```
Žingsnis 4 būsena: (0,2,3,1,4,5,7,8,6)
  Galimi veiksmai: DOWN, RIGHT

  DOWN → (1,2,3,0,4,5,7,8,6)  ← dar nematyta → į frontier ✅
  RIGHT→ (2,0,3,1,4,5,7,8,6)  ← jau explored  → PRALEISTI ❌
                                  (tai buvo žingsnis 3!)
```

Be `explored` aibės BFS suktųsi ratu amžinai.

---

## Sprendimo atstatymas: `solution()`

```python
def solution(self):
    return [node.action for node in self.path()[1:]]

def path(self):
    node, path_back = self, []
    while node:
        path_back.append(node)
        node = node.parent          # ← einame atgal per parent nuorodas
    return list(reversed(path_back))
```

Kiekvienas `Node` saugo nuorodą į `parent`. Kai randamas tikslas,
einame atgal per grandinę: `tikslas → ... → pradžia`, surenkame `action` kiekviename žingsnyje.

```
Node(depth=8, action='DOWN')
  └─ parent: Node(depth=7, action='RIGHT')
       └─ parent: Node(depth=6, action='RIGHT')
            └─ parent: Node(depth=5, action='DOWN')
                 └─ ... → Node(depth=0, action=None)  ← šaknis
```

`solution()` grąžina: `['UP', 'LEFT', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'DOWN']`
