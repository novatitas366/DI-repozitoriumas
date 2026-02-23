# NQueensProblem.py — pilnas paaiškinimas

## Kas yra N karalienių uždavinys?

N karalienių uždavinys — klasikinis kombinatorikos uždavinys: reikia **N karalienių išdėstyti ant N×N šachmatų lentos** taip, kad **nė viena karalienė nekirstų kitos** (nei eilutėje, nei stulpelyje, nei įstrižainėje). Programa sprendžia šį uždavinį kaip **paieškos uždavinį**.

---

## Importuojami failai ir ką jie daro

`from search import *` — importuoja viską iš `lib/search.py`. Iš ten naudojami:
[[LD1_analize]]

| Kas importuojama | Paskirtis |
|---|---|
| `class Problem` | Abstrakti bazinė klasė visiems paieškos uždaviniams |
| `class Node` | Paieškos medžio mazgas: saugo `state`, `parent`, `action`, `path_cost`, `depth` |
| `class NQueensProblem` | Konkretus N karalienių uždavinio apibrėžimas (paveldi `Problem`) |
| `best_first_graph_search()` | Paieškos algoritmas su prioritetine eile pagal heuristinę funkciją |
| `breadth_first_graph_search()` | Paieška platyn (BFS) su dviguba eile (deque) |
| `recursive_best_first_search()` | Rekursyvi geriausio-pirmojo paieška (RBFS) |

`search.py` importuoja iš `utils.py` (pagalbinės funkcijos: `PriorityQueue`, `memoize` ir kt.) ir iš `maps.py`.

---

## Pirminė būsena (initial state)

```python
nq_problem = NQueensProblem(5)
# initial state = (-1, -1, -1, -1, -1)
```

**Pirminė būsena** — tai **N ilgio kortežas (tuple)**, kur visos reikšmės lygios `-1`.

- **Indeksas kortežo** = stulpelio numeris (0..N-1)
- **Reikšmė** = eilutės numeris, kurioje stovi karalienė (arba `-1`, jei stulpelis dar tuščias)

N=5 atveju: `(-1, -1, -1, -1, -1)` — lenta visiškai tuščia.

## Galinė būsena (goal state)

**Galinė būsena** — kortežas, kur:
1. **Nėra `-1`** — visi stulpeliai užpildyti
2. **Nėra konfliktų** — nė viena pora karalienių nesikerta

Tikrinama metodu `goal_test(state)`:
```python
def goal_test(self, state):
    if state[-1] == -1:      # jei paskutinis stulpelis tuščias → ne tikslas
        return False
    return not any(self.conflicted(state, state[col], col)
                   for col in range(len(state)))
```

N=5 programos sprendimas: `[4, 1, 3, 0, 2]`
Tai reiškia galinę būseną: `(4, 1, 3, 0, 2)`:
- stulpelis 0 → eilutė 4
- stulpelis 1 → eilutė 1
- stulpelis 2 → eilutė 3
- stulpelis 3 → eilutė 0
- stulpelis 4 → eilutė 2

## Kintamieji būsenos aprašymui

| Kintamasis | Tipas | Reikšmė |
|---|---|---|
| `state` | `tuple` ilgio N | Visa būsena — karalienių eilučių numeriai pagal stulpelius |
| `state[c]` | `int` | Eilutė, kurioje stovi karalienė stulpelyje `c` (-1 = tuščia) |
| `N` | `int` | Lentos dydis (karalienių skaičius) |

---

## 5 būsenos su kintamųjų reikšmėmis (N=5, sprendimas [4,1,3,0,2])

Žemiau pavaizduotos sprendimo kelio būsenos. **Q** = karalienė, **·** = tuščia.

### Būsena 0 — Pradinė (initial)
```
state = (-1, -1, -1, -1, -1)

     stulp: 0   1   2   3   4
eilutė 0: [  · ][ · ][ · ][ · ][ · ]
eilutė 1: [  · ][ · ][ · ][ · ][ · ]
eilutė 2: [  · ][ · ][ · ][ · ][ · ]
eilutė 3: [  · ][ · ][ · ][ · ][ · ]
eilutė 4: [  · ][ · ][ · ][ · ][ · ]
```
Lenta tuščia. Nė vienas stulpelis neužpildytas.

---

### Būsena 1 — po 1 veiksmo (action=4)
```
state = (4, -1, -1, -1, -1)

     stulp: 0   1   2   3   4
eilutė 0: [  · ][ · ][ · ][ · ][ · ]
eilutė 1: [  · ][ · ][ · ][ · ][ · ]
eilutė 2: [  · ][ · ][ · ][ · ][ · ]
eilutė 3: [  · ][ · ][ · ][ · ][ · ]
eilutė 4: [  Q ][ · ][ · ][ · ][ · ]
```
Karalienė padėta stulpelyje 0, eilutėje 4.

---

### Būsena 2 — po 2 veiksmų (action=1)
```
state = (4, 1, -1, -1, -1)

     stulp: 0   1   2   3   4
eilutė 0: [  · ][ · ][ · ][ · ][ · ]
eilutė 1: [  · ][ Q ][ · ][ · ][ · ]
eilutė 2: [  · ][ · ][ · ][ · ][ · ]
eilutė 3: [  · ][ · ][ · ][ · ][ · ]
eilutė 4: [  Q ][ · ][ · ][ · ][ · ]
```
Karalienė padėta stulpelyje 1, eilutėje 1.

---

### Būsena 3 — po 3 veiksmų (action=3)
```
state = (4, 1, 3, -1, -1)

     stulp: 0   1   2   3   4
eilutė 0: [  · ][ · ][ · ][ · ][ · ]
eilutė 1: [  · ][ Q ][ · ][ · ][ · ]
eilutė 2: [  · ][ · ][ · ][ · ][ · ]
eilutė 3: [  · ][ · ][ Q ][ · ][ · ]
eilutė 4: [  Q ][ · ][ · ][ · ][ · ]
```

---

### Būsena 4 — po 4 veiksmų (action=0)
```
state = (4, 1, 3, 0, -1)

     stulp: 0   1   2   3   4
eilutė 0: [  · ][ · ][ · ][ Q ][ · ]
eilutė 1: [  · ][ Q ][ · ][ · ][ · ]
eilutė 2: [  · ][ · ][ · ][ · ][ · ]
eilutė 3: [  · ][ · ][ Q ][ · ][ · ]
eilutė 4: [  Q ][ · ][ · ][ · ][ · ]
```

---

### Būsena 5 — Galinė (goal), po 5 veiksmų (action=2)
```
state = (4, 1, 3, 0, 2)   ← SPRENDIMAS

     stulp: 0   1   2   3   4
eilutė 0: [  · ][ · ][ · ][ Q ][ · ]
eilutė 1: [  · ][ Q ][ · ][ · ][ · ]
eilutė 2: [  · ][ · ][ · ][ · ][ Q ]
eilutė 3: [  · ][ · ][ Q ][ · ][ · ]
eilutė 4: [  Q ][ · ][ · ][ · ][ · ]
```
Visos 5 karalienės išdėstytos — nė viena nekerta kitos.

---

## Kaip veikia paieška — eilė (queue) ir jos tipas

Paieška vykdoma per `Node` objektus. Kiekvienas `Node` saugo:
- `state` — dabartinė lento būsena (kortežas)
- `parent` — iš kurio mazgo atėjome
- `action` — kokį veiksmą atlikome (kurią eilutę pasirinkome)
- `path_cost` — kaina iki šio mazgo
- `depth` — gylis medyje

### Paieška platyn (BFS) — naudoja `deque` (dvigubą eilę)

```python
frontier = deque([node])   # FIFO eilė
# ...
node = frontier.popleft()  # imame iš priekio
frontier.append(child)     # dedame į galą
```

`deque` + `popleft()` → **FIFO** (pirmasis įeinantis = pirmasis išeinantis).
Tai reiškia: **pirmiausia peržiūrimi sekliausi mazgai** → paieška platyn.
BFS garantuoja **trumpiausio kelio** (pagal veiksmų skaičių) radimą.

### Paieška į gylį (DFS) — naudoja `list` kaip steką

```python
frontier = [Node(problem.initial)]  # stack (stekas)
# ...
node = frontier.pop()               # imame iš galo (LIFO)
frontier.extend(node.expand(problem))
```

`list` + `pop()` → **LIFO** (paskutinis įeinantis = pirmasis išeinantis).
Tai reiškia: **pirmiausia peržiūrimi giliausiai einantys mazgai** → paieška į gylį.

### Paieška pagal prioritetą (Best-First) — naudoja `PriorityQueue`

```python
frontier = PriorityQueue('min', f)  # eilė pagal f reikšmę
node = frontier.pop()               # imame mazgą su mažiausia f reikšme
```

Kiekvienam mazgui apskaičiuojama funkcija `f(node)` ir eilė rūšiuojama pagal ją.
Šiame uždavinyje: `f(n) = h(n)` — **godžioji (greedy) geriausio-pirmojo paieška**.

---

## Heuristika h(n)

```python
def h(self, node):
    """Return number of conflicting queens for a given node"""
    num_conflicts = 0
    for (r1, c1) in enumerate(node.state):
        for (r2, c2) in enumerate(node.state):
            if (r1, c1) != (r2, c2):
                num_conflicts += self.conflict(r1, c1, r2, c2)
    return num_conflicts
```

**h(n) = kertančių karalienių porų skaičius** (kuo mažiau — tuo geriau, tikslas = 0).

Svarbu: `enumerate(state)` iteruoja per `(indeksas, reikšmė)`, čia:
- `c` = indeksas = stulpelis
- `r` = reikšmė = eilutė

Kai `state[c] == -1` (stulpelis tuščias), ta pozicija taip pat dalyvaus skaičiavime (karalienė tariamai eilutėje -1), todėl heuristika tiksliausia visiškai užpildytose būsenose.

### Kitos galimos heuristikos

| Heuristika | Aprašymas |
|---|---|
| **h(n) = kertančių porų sk.** | Šiame kode naudojama. Greita, bet ne visada tiksli ne pilnose būsenose |
| **h(n) = likusių konfliktų sk. + likusių stulpelių sk.** | Tikslesnė informuota heuristika |
| **h(n) = 0** | Taptu kaip UCS (vienodų kaštų paieška) |
| **A\*: f(n) = g(n) + h(n)** | Kaina iki mazgo + heuristika — optimalus algoritmas |

---

## Naudojamas algoritmas: `best_first_graph_search`

```python
solution = best_first_graph_search(nq_problem, lambda n: nq_problem.h(n)).solution()
```

### Veikimo principas žingsnis po žingsnio:

1. **Sukuriamas pradinis mazgas**: `Node(state=(-1,-1,-1,-1,-1))`
2. **Mazgas dedamas į `PriorityQueue`** rūšiuojamą pagal `h(n)`
3. **Pagrindinė kilpa**:
   - Išimamas mazgas su **mažiausia `h` reikšme**
   - Jei `goal_test(state)` = True → grąžinamas sprendimas
   - Mazgo būsena įtraukiama į `explored` (aplankytos būsenos)
   - Išplečiami vaikai per `node.expand(problem)`:
     - kiekvienam galimam veiksmui iš `actions(state)` sukuriamas vaikas
     - vaikas dedamas į eilę, jei jo būsena dar neaplankyta
4. **`node.solution()`** — eina atgal per `parent` rodykles ir surenka `action` reikšmes → sprendimo veiksmų sąrašas

### `actions(state)` — kaip renkamos galimos eilutės

```python
def actions(self, state):
    if state[-1] != -1:
        return []              # visos kolonos užpildytos
    col = state.index(-1)      # kairiausia tuščia kolona
    return [row for row in range(self.N)
            if not self.conflicted(state, row, col)]
```

Algoritmas **visada pildo stulpelius iš kairės į dešinę** ir siūlo tik tokias eilutes, kurios **nesukelia konflikto** su jau padėtomis karalienėmis. Tai sumažina paieškos erdvę.

### Konflikto tikrinimas

```python
def conflict(self, row1, col1, row2, col2):
    return (row1 == row2 or           # ta pati eilutė
            col1 == col2 or           # tas pats stulpelis
            row1 - col1 == row2 - col2 or  # ta pati \ įstrižainė
            row1 + col1 == row2 + col2)    # ta pati / įstrižainė
```

---

## Failo struktūra

| Eilutės | Paskirtis |
|---|---|
| 1–14 | Uždavinio sprendimas: sukuria `NQueensProblem`, vykdo paiešką, spausdina sprendinį |
| 20–41 | `plot_solution()` — paprastas piešimas matplotlib: raidė „Q" ant tinklelio |
| 48–74 | `plot_NQueens()` — grafinė vizualizacija su karalienės paveikslėliu (veikia tik N=8) |
| 76–88 | Užkomentuotas interaktyvus vartotojo klausimas |

---

## Pastabos

- Komentare kode: **N=30 → >30 min** skaičiavimo laiko — eksponentinis augimas
- `plot_NQueens` aktyvuojama tik `number_of_queens == 8`, nes paveikslėlio koordinatės apskaičiuotos 8×8 lentai
- Pylance rodo įspėjimą `NQueensProblem is not defined` — nes jis importuojamas su `*`, o statiniai analizatoriai negali jo aptikti. Paleidus programą — veikia teisingai
- Užkomentuotos alternatyvos:
  - `breadth_first_graph_search` — veiks, bet lėtai (neišnaudoja heuristikos)
  - `recursive_best_first_search` — rekursyvi RBFS, taupa atmintį bet lėtesnė
