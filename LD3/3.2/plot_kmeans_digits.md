# `plot_kmeans_digits.py` — K-Means grupavimas ranka rašytų skaitmenų duomenims

## Apžvalga

Šis failas demonstruoja **K-Means klasterizacijos** algoritmą naudojant `scikit-learn` biblioteką. Pagrindinis tikslas — palyginti tris skirtingus K-Means inicializacijos metodus pagal greitį ir rezultatų kokybę.

---

## Duomenų rinkinys

Naudojamas `sklearn.datasets.load_digits` duomenų rinkinys:
- **1797 pavyzdžiai** (ranka rašytų skaitmenų nuotraukos)
- **64 požymiai** (8×8 pikselių vaizdas, išskleistas į vektorių)
- **10 klasių** (skaitmenys nuo 0 iki 9)

---

## Įvertinimo metrikos

Kadangi tikrosios klasės žinomos, naudojamos šios grupavimo kokybės metrikos:

| Santrumpa | Pavadinimas |
|-----------|-------------|
| `homo` | Homogeniškumo balas |
| `compl` | Pilnumo balas |
| `v-meas` | V-matas |
| `ARI` | Pakoreguotas Rand indeksas |
| `AMI` | Pakoreguota abipusė informacija |
| `silhouette` | Silueto koeficientas |

---

## Lyginami inicializacijos metodai

### 1. `k-means++`
- Stochastinis metodas — centrų pradinė padėtis parenkama tikimybiškai, preferuojant tolimesnius taškus
- Paleidžiamas **4 kartus** (`n_init=4`), išsaugomas geriausias rezultatas

### 2. `random` (atsitiktinė inicializacija)
- Pradiniai centroidai parenkami visiškai atsitiktinai
- Taip pat paleidžiamas **4 kartus**

### 3. `PCA-based` (PCA pagrindu)
- Naudojami **PCA komponentai** kaip pradiniai centroidai
- Deterministinis metodas — pakanka **1 paleidimo** (`n_init=1`)

Kiekvienas metodas testuojamas per `bench_k_means()` funkciją, kuri:
1. Sukuria `Pipeline`: `StandardScaler → KMeans`
2. Treniruoja modelį ir matuoja laiką
3. Apskaičiuoja visas metrikas ir atspausdina rezultatų eilutę

---

## Vizualizacija

Rezultatai vaizduojami **2D erdvėje** naudojant PCA projekciją (iš 64 matmenų → 2):

- **Spalvotos sritys** — K-Means sprendimų ribos (Voronoi diagrama)
- **Juodi taškai** — tikrų duomenų pavyzdžiai
- **Balti ×** — klasterių centroidai

```
KMeans su k-means++ inicializacija → fit ant 2D PCA duomenų → meshgrid sprendimų ribų braižymas
```

---

## Pagrindinė schema

```
load_digits()
    │
    ▼
bench_k_means()  ←  k-means++ / random / PCA-based
    │
    ▼
Metrikos lentelė (terminale)
    │
    ▼
PCA(2D) → KMeans → Vizualizacija (matplotlib)
```
