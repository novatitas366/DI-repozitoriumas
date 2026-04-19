# Bajeso tinklas: Studento egzamino rezultatas

## Scenarijus

Studento sėkmė egzamine priklauso nuo to, ar jis mokėsi ir ar gerai išsimiegojo. Mokymasis priklauso nuo motyvacijos ir to, ar buvo vakarėlis. Miegas taip pat priklauso nuo vakarėlio. Galutinis rezultatas – egzamino pažymys, nuo kurio priklauso, ar studentas gaus stipendiją.

## Tinklo struktūra

```
Motyvacija       Vakarėlis
     \\          /       \\
      \\        /         \\
       v      v           v
       Mokėsi         Išsimiegojo
           \\            /
            \\          /
             v        v
            Egzaminas
                |
                v
            Stipendija
```

**Briaunos:**
- `Motyvacija` → `Mokėsi`
- `Vakarėlis` → `Mokėsi`
- `Vakarėlis` → `Išsimiegojo`
- `Mokėsi` → `Egzaminas`
- `Išsimiegojo` → `Egzaminas`
- `Egzaminas` → `Stipendija`

## Kintamieji

Visi kintamieji turi dvi reikšmes: `"1"` (taip) ir `"0"` (ne).

| ID  | Kintamasis   | Tipas        | Tėvai                  |
|-----|--------------|--------------|------------------------|
| 1   | Motyvacija   | Šaknis       | –                      |
| 2   | Vakarėlis    | Šaknis       | –                      |
| 3   | Mokėsi       | Vidinis      | Motyvacija, Vakarėlis  |
| 4   | Išsimiegojo  | Vidinis      | Vakarėlis              |
| 5   | Egzaminas    | Vidinis      | Mokėsi, Išsimiegojo    |
| 11  | Stipendija   | Lapas        | Egzaminas              |

> **Pastaba dėl ID:** pavyzdiniame formate ID koduotė naudoja vieną skaitmenį prie reikšmės (pvz., `id=6` → `60`/`61`). Todėl `Stipendija` gavo `id=11`, kad nesusikirstų su `id=1` (Motyvacija → `10`/`11`).

## Sąlyginės tikimybės (CPT)

### Motyvacija (a priori)

| Motyvacija | P    |
|------------|------|
| taip (10)  | 0.6  |
| ne (11)    | 0.4  |

### Vakarėlis (a priori)

| Vakarėlis | P    |
|-----------|------|
| taip (20) | 0.3  |
| ne (21)   | 0.7  |

### Mokėsi | Motyvacija, Vakarėlis

| Motyvacija | Vakarėlis | P(Mokėsi=taip) | P(Mokėsi=ne) |
|------------|-----------|----------------|--------------|
| taip       | taip      | 0.50           | 0.50         |
| taip       | ne        | 0.95           | 0.05         |
| ne         | taip      | 0.10           | 0.90         |
| ne         | ne        | 0.40           | 0.60         |

Motyvuotas studentas be vakarėlio beveik tikrai mokysis (0.95). Vakarėlis stipriai mažina mokymosi tikimybę.

### Išsimiegojo | Vakarėlis

| Vakarėlis | P(Išsimiegojo=taip) | P(Išsimiegojo=ne) |
|-----------|---------------------|-------------------|
| taip      | 0.20                | 0.80              |
| ne        | 0.90                | 0.10              |

### Egzaminas | Mokėsi, Išsimiegojo

| Mokėsi | Išsimiegojo | P(Išlaikė) | P(Neišlaikė) |
|--------|-------------|------------|--------------|
| taip   | taip        | 0.95       | 0.05         |
| taip   | ne          | 0.75       | 0.25         |
| ne     | taip        | 0.50       | 0.50         |
| ne     | ne          | 0.15       | 0.85         |

Didžiausia tikimybė išlaikyti (0.95) – kai studentas ir mokėsi, ir išsimiegojo. Mažiausia (0.15) – kai nei mokėsi, nei miegojo.

### Stipendija | Egzaminas

| Egzaminas | P(Stipendija=taip) | P(Stipendija=ne) |
|-----------|--------------------|------------------|
| išlaikė   | 0.85               | 0.15             |
| neišlaikė | 0.05               | 0.95             |

## JSON formato logika

Kiekvienas mazgas turi:
- `id`, `title` – identifikatorius ir pavadinimas
- `x`, `y`, `px`, `py` – koordinatės grafiniam atvaizdavimui
- `values` – galimos reikšmės (`["1", "0"]`)
- `tbl` – sąlyginių tikimybių lentelė, kur raktai yra `{parent_id}{value}` formos (pvz., `10` = Motyvacija=taip, `11` = Motyvacija=ne)
- `index`, `weight` – pagalbiniai laukai

Briaunos (`edges`) yra pilnos mazgų objektų kopijos su `source` ir `target` laukais – taip pat kaip pavyzdiniame faile.

## Pavyzdinis klausimas inferencijai

**Klausimas:** Kokia tikimybė, kad studentas gaus stipendiją, jei žinome, kad vakar vyko vakarėlis?

Intuityviai: vakarėlis → mažesnė tikimybė mokytis ir išsimiegoti → mažesnė tikimybė išlaikyti → mažesnė tikimybė gauti stipendiją. Tinklas leidžia tai apskaičiuoti tiksliai naudojant marginalizaciją per nematomus kintamuosius.
