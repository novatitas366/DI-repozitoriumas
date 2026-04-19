# Neapibrėžtumo pavyzdys: Studento egzamino išlaikymas

## 1. Gripo pavyzdžio analizė (iš paskaitos)

Paskaitoje pateikta jungtinė tikimybių lentelė su trimis Bool'io kintamaisiais: **Gripas**, **GalvosSkausmas**, **Temperatūra**. Lentelėje yra 2³ = 8 galimi pasaulio būsenos variantai, kurių tikimybių suma lygi 1:

$$0.108 + 0.012 + 0.072 + 0.008 + 0.016 + 0.064 + 0.144 + 0.576 = 1.000$$

**Nesąlyginė (marginalinė) tikimybė** gaunama sumuojant atitinkamas jungtines tikimybes. Pavyzdžiui, tikimybė, kad žmogus serga gripu:

$$P(Gripas) = 0.108 + 0.012 + 0.072 + 0.008 = 0.20$$

Panašiai galvos skausmo tikimybė:

$$P(GalvosSkausmas) = 0.108 + 0.012 + 0.016 + 0.064 = 0.20$$

**Sąlyginė tikimybė** skaičiuojama pagal formulę:

$$P(A \mid B) = \frac{P(A \land B)}{P(B)}$$

Pavyzdžiui, tikimybė, kad žmogus serga gripu, jei jis turi galvos skausmą:

$$P(Gripas \mid GalvosSkausmas) = \frac{P(Gripas \land GalvosSkausmas)}{P(GalvosSkausmas)} = \frac{0.108 + 0.012}{0.20} = \frac{0.12}{0.20} = 0.60$$

Matome, kad žinojimas apie galvos skausmą padidina gripo tikimybę nuo 0.20 iki 0.60 — tai ir yra sąlyginės tikimybės esmė.

---

## 2. Pasirinkta dalykinė sritis: Studento egzamino išlaikymas

Pasirinkau tris loginius (Boolean) kintamuosius:

- **M** — *Mokėsi* (studentas reguliariai mokėsi semestro metu)
- **I** — *Išsimiegojo* (studentas prieš egzaminą gerai išsimiegojo)
- **L** — *Laikė* (studentas išlaikė egzaminą)

### Jungtinė tikimybių lentelė

|               | **Išsimiegojo (I)** |                 | **¬Išsimiegojo (¬I)** |                 |
| ------------- | ------------------- | --------------- | --------------------- | --------------- |
|               | **Laikė (L)**       | **¬Laikė (¬L)** | **Laikė (L)**         | **¬Laikė (¬L)** |
| **Mokėsi (M)**   | 0.30                | 0.05            | 0.15                  | 0.10            |
| **¬Mokėsi (¬M)** | 0.04                | 0.11            | 0.02                  | 0.23            |

Patikrinimas: $0.30 + 0.05 + 0.15 + 0.10 + 0.04 + 0.11 + 0.02 + 0.23 = 1.00$ ✓

---

## 3. Tikimybių skaičiavimas

### Nesąlyginė tikimybė — P(Laikė)

Sumuojame visas eilutes, kuriose įvykis **L** yra teisingas:

$$P(L) = P(M \land I \land L) + P(M \land \neg I \land L) + P(\neg M \land I \land L) + P(\neg M \land \neg I \land L)$$

$$P(L) = 0.30 + 0.15 + 0.04 + 0.02 = 0.51$$

Taigi bendra tikimybė, kad atsitiktinai pasirinktas studentas išlaikys egzaminą, yra **0.51** (51%).

Papildomai galime apskaičiuoti:

$$P(M) = 0.30 + 0.05 + 0.15 + 0.10 = 0.60$$

$$P(I) = 0.30 + 0.05 + 0.04 + 0.11 = 0.50$$

### Sąlyginė tikimybė — P(L | M ∧ I)

Klausimas: *kokia tikimybė, kad studentas išlaikys egzaminą, jei jis ir mokėsi, ir išsimiegojo?*

$$P(L \mid M \land I) = \frac{P(L \land M \land I)}{P(M \land I)}$$

Skaitiklis paimamas tiesiai iš lentelės:

$$P(L \land M \land I) = 0.30$$

Vardiklis — sumuojame eilutes su M ir I (nepriklausomai nuo L):

$$P(M \land I) = 0.30 + 0.05 = 0.35$$

Tuomet:

$$P(L \mid M \land I) = \frac{0.30}{0.35} \approx 0.857$$

### Palyginimui — P(L | ¬M ∧ ¬I)

$$P(L \mid \neg M \land \neg I) = \frac{0.02}{0.02 + 0.23} = \frac{0.02}{0.25} = 0.08$$

---

## 4. Interpretacija

Nesąlyginė tikimybė rodo, kad „vidutinis" studentas egzaminą išlaiko su 51% tikimybe. Tačiau kai turime papildomos informacijos (studentas mokėsi ir išsimiegojo), tikimybė šoka iki **~85.7%**, o priešingu atveju (nei mokėsi, nei išsimiegojo) nukrenta iki vos **8%**. Tai gerai iliustruoja, kaip papildomi įrodymai (evidence) keičia mūsų tikėjimą apie įvykį — lygiai taip pat, kaip gripo pavyzdyje galvos skausmas padidino gripo tikimybę nuo 0.20 iki 0.60.
