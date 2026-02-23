# Eight Puzzle — pilnas paaiškinimas

## Kas tai?

**Eight Puzzle** (Aštuonių figūrų dėlionė) — klasikinė paieškos problema.
3×3 lentoje yra 8 sunumeruoti plyteliai ir **viena tuščia vieta (0)**.
Tikslas: perkeliant plyteles į tuščią vietą, sudėlioti jas į teisingą tvarką.

```
Pradžia:          Tikslas:
2 4 3             1 2 3
1 5 6    →→→      4 5 6
7 8 _             7 8 _
```

---

## Būsenos atvaizdavimas

Lenta vaizduojama kaip **9 elementų kortežas (tuple)**:

```python
(2, 4, 3, 1, 5, 6, 7, 8, 0)
```

Indeksai atitinka pozicijas lentoje:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

`0` — tuščia vieta.

---

## Kodas: `EightPuzzle.py`

```python
puzzle = EightPuzzle((2, 4, 3, 1, 5, 6, 7, 8, 0))
solution = breadth_first_graph_search(puzzle).solution()
print(f'{solution}')
```

1. Sukuriamas `EightPuzzle` objektas su pradinė būsena `(2,4,3,1,5,6,7,8,0)`.
2. Sprendžiamas naudojant **BFS** (breadth-first graph search).
3. `.solution()` grąžina veiksmų sąrašą, pvz.: `['UP', 'LEFT', 'DOWN', ...]`

---

## Klasė `EightPuzzle` (iš `search.py`)

```python
class EightPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)
```

Paveldi abstrakčią klasę `Problem`. Tikslinė būsena pagal nutylėjimą: `(1,2,3,4,5,6,7,8,0)`.

---

### `find_blank_square(state)`

```python
def find_blank_square(self, state):
    return state.index(0)
```

Randa tuščios vietos indeksą kortežе. Pvz., jei `0` yra pozicijoje 8 — grąžina `8`.

---

### `actions(state)`

```python
def actions(self, state):
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    index_blank_square = self.find_blank_square(state)

    if index_blank_square % 3 == 0:
        possible_actions.remove('LEFT')   # kairės kraštinė
    if index_blank_square < 3:
        possible_actions.remove('UP')     # viršutinė eilutė
    if index_blank_square % 3 == 2:
        possible_actions.remove('RIGHT')  # dešinės kraštinė
    if index_blank_square > 5:
        possible_actions.remove('DOWN')   # apatinė eilutė
    return possible_actions
```

Grąžina galimus veiksmus iš dabartinės būsenos.
**Veiksmas** — kryptis, kuria **tuščia vieta juda** (arba kitaip: plytelė juda priešinga kryptimi).

Kraštinių tikrinimas pagal indeksą:

| Sąlyga | Reiškia |
|---|---|
| `idx % 3 == 0` | kairė kolona (0,3,6) — negalima judėti KAIRĖN |
| `idx < 3` | viršutinė eilutė (0,1,2) — negalima judėti AUKŠTYN |
| `idx % 3 == 2` | dešinė kolona (2,5,8) — negalima judėti DEŠINĖN |
| `idx > 5` | apatinė eilutė (6,7,8) — negalima judėti ŽEMYN |

---

### `result(state, action)`

```python
def result(self, state, action):
    blank = self.find_blank_square(state)
    new_state = list(state)

    delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
    neighbor = blank + delta[action]
    new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

    return tuple(new_state)
```

Atlieka veiksmą: **sukeičia tuščią vietą su kaimynine plytele**.

`delta` žodynas nurodo, kiek indeksas pasikeičia kiekviena kryptimi:
- `UP` → `-3` (eisime eilute aukštyn = 3 pozicijos atgal)
- `DOWN` → `+3`
- `LEFT` → `-1`
- `RIGHT` → `+1`

---

### `goal_test(state)`

```python
def goal_test(self, state):
    return state == self.goal
```

Tiesiog palygina dabartinę būseną su tiksline. Grąžina `True` jei išspręsta.

---

### `h(node)` — euristika

```python
def h(self, node):
    return sum(s != g for (s, g) in zip(node.state, self.goal))
```

**Neteisingai patalpintų plytelių skaičius** — kiek plytelių nėra savo tikslinėje pozicijoje.
Naudojama su `best_first_graph_search` arba `astar_search`.

Pvz., jei 3 plytelės ne savo vietoje → `h = 3`.

> `check_solvability` metodas yra užkomentuotas — jis tikrintų ar pradinė būsena apskritai yra išsprendžiama (per inversijų skaičių), bet šiuo metu nenaudojamas.

---

## Kaip veikia paieška: `search.py`

### Abstrakti klasė `Problem`

```python
class Problem:
    def __init__(self, initial, goal=None): ...
    def actions(self, state): ...       # ką galima daryti
    def result(self, state, action): ...# kas nutiks
    def goal_test(self, state): ...     # ar pasiektas tikslas
    def path_cost(self, c, s1, a, s2): return c + 1  # kaina (numatyta: kiekvienas žingsnis = 1)
```

`EightPuzzle` paveldi šią klasę ir implementuoja jos metodus.

---

### Klasė `Node`

```python
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0
```

Kiekvienas paieškos medžio mazgas saugo:
- `state` — dabartinę būseną
- `parent` — iš kur atėjome
- `action` — koks veiksmas atvedė čia
- `path_cost` — bendra kelionės kaina

#### `expand(problem)`

```python
def expand(self, problem):
    return [self.child_node(problem, action)
            for action in problem.actions(self.state)]
```

Sugeneruoja visus vaikų mazgus iš dabartinio mazgo (visi galimi veiksmai).

#### `solution()`

```python
def solution(self):
    return [node.action for node in self.path()[1:]]
```

Eina atgal per `parent` nuorodas iki šaknies ir surenka veiksmų sąrašą → tai ir yra sprendimas.

---

## BFS algoritmas (`breadth_first_graph_search`)

```python
def breadth_first_graph_search(problem, step_limits=-1):
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node                      # pradinė būsena jau yra tikslas

    frontier = deque([node])             # FIFO eilė
    explored = set()                     # aplankytos būsenos
    step_num = 0

    while frontier:
        step_num += 1
        node = frontier.popleft()        # imame iš kairės (seniausia)

        if step_limits > 0 and step_num >= step_limits:
            return node                  # debug sustojimas

        explored.add(node.state)         # žymime kaip aplankytą

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child         # rastas tikslas!
                frontier.append(child)   # dedame į dešinę (nauja)

    return None                          # sprendimo nėra
```

### BFS savybės

| Savybė | Reikšmė |
|---|---|
| **Pilnumas** | Taip — visada ras sprendimą jei jis egzistuoja |
| **Optimalumas** | Taip — randa trumpiausią kelią (mažiausiai žingsnių) |
| **Laiko sudėtingumas** | O(b^d), kur b — šakojimosi faktorius, d — gylis |
| **Erdvės sudėtingumas** | O(b^d) — saugo visus frontier mazgus |

Eight Puzzle atveju: `b ≈ 3` (vidutiniškai 3 galimi veiksmai), gylis priklauso nuo pradinės būsenos.

---

## Alternatyva: Greedy Best-First paieška

```python
# solution = best_first_graph_search(puzzle, lambda n: puzzle.h(n)).solution()
```

Naudoja euristiką `h(n)` (neteisingų plytelių skaičius), kad greičiau rastų tikslą.
**Nėra optimali** — gali rasti ilgesnį kelią, bet paprastai **greitesnė** nei BFS.

---

## Vykdymo pavyzdys

Pradinė būsena: `(2, 4, 3, 1, 5, 6, 7, 8, 0)`

```
2 4 3
1 5 6
7 8 _
```

BFS suranda optimalų veiksmų sąrašą, pvz.:
```
['UP', 'UP', 'LEFT', 'DOWN', 'RIGHT', ...]
```

Kiekvienas veiksmas rodo, kuria kryptimi juda **tuščia vieta**.
