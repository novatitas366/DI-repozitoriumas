# DI-repozitoriumas

Dirbtinio intelekto laboratorinių darbų repozitorija.

---

## LD1 — Paieška būsenų erdvėje

Klasikinių AI paieškos uždavinių implementacijos, pagrįstos **AIMA** (*Artificial Intelligence: A Modern Approach*) biblioteka.

### Failai

| Failas | Aprašymas |
|--------|-----------|
| `search.py` | Bazinės klasės (`Problem`, `Node`) ir paieškos algoritmai (BFS, Best-First, RBFS) |
| `WaterJugProblem.py` | Vandens ąsočių uždavinys — rasti 2L naudojant 4L ir 3L ąsočius |
| `EightPuzzle_graph.py` | Aštuonių figūrų dėlionė — 3×3 lenta, plytelės išdėliojamos į teisingą tvarką |
| `NQueensProblem_graph.py` | N karalienių uždavinys — N karalienių ant N×N lentos be konfliktų |

### Naudojami algoritmai

- **BFS** (Paieška platyn) — garantuoja trumpiausią kelią pagal žingsnių skaičių; naudoja FIFO eilę (`deque`)
- **Greedy Best-First** — naudoja heuristinę funkciją `h(n)`, greitesnė bet neoptimali
- **RBFS** — rekursinė geriausio-pirmojo paieška, taupanti atmintį

### Uždaviniai

**Vandens ąsočių uždavinys** — pradinė būsena `(0, 0)`, tikslas `A = 2L`. BFS randa optimalų sprendimą per 6 žingsnius. Vizualizuojamas visas būsenų grafas (`water_jug_graph.png`).

**Aštuonių figūrų dėlionė** — pradinė būsena `(2,4,3,1,5,6,7,8,0)`, tikslas `(1,2,3,4,5,6,7,8,0)`. BFS suranda sprendimą per 8 žingsnius.

**N karalienių uždavinys** — sprendžiamas Best-First paieška su heuristika `h(n) = kertančių karalienių porų skaičius`. N=5 sprendimas: `[4, 1, 3, 0, 2]`.

### Dokumentacija

- `BFS_paaiškinimas.md` — BFS algoritmo veikimas, pseudokodas, savybės
- `EightPuzzle_paaiškinimas.md` — Eight Puzzle klasės metodai, BFS schema žingsnis po žingsnio
- `NQueensProblem_paaiškinimas.md` — N karalienių uždavinio struktūra, heuristika, paieškos eilės tipai
- `WaterJugProblem_paaiškinimas.md` — Vandens ąsočių uždavinio veiksmų logika, BFS ir Greedy palyginimas
- `Paieška_Busenų_Erdveje.pptx` — pristatymo skaidrės

---

## LD2 — Grafų generavimo algoritmai

Grafų generavimo algoritmų implementacija C++ kalba (`main.cpp`).
