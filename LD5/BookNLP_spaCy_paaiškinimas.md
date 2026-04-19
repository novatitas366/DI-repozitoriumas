# BookNLP_spaCy.ipynb — Lingvistinė anotacija su spaCy ir WordNet

## Apžvalga

Šis notebook'as yra **antrasis** grandinėje — tęsia ten, kur baigė `BookNLP.ipynb`. Jis paima paruoštą pastraipų TSV failą ir atlieka išsamią lingvistinę analizę, naudodamas `spaCy` kalbos modelį bei `WordNet` leksinę duomenų bazę.

---

## Kas gaunama po vykdymo

| Rezultatas | Aprašymas |
|---|---|
| `df_book_token_spacy` | Kiekvienas žodis (tokenas) su POS, priklausomybėmis, entiteto tipu, WordNet informacija ir kt. |
| `df_book_entity_spacy` | Visi atpažinti pavadinimai (asmenys, vietos, organizacijos ir kt.) su pozicijomis |
| `df_book_noun_chunk_spacy` | Daiktavardinės frazės (noun chunks) su šaknimi ir pozicijomis |
| `df_book_token_spacy_<book_code>.tsv` | Eksportuotas tokenų failas Google Drive |

---

## Darbo eiga žingsnis po žingsnio

### 1. Aplinkos paruošimas

- Importuojamos bibliotekos: `pandas`, `nltk` (WordNet ir Lesk WSD), `spaCy`, `requests`, `json`.
- `nltk.download('wordnet')` — atsisiunčiamas WordNet žodynas.
- Montuojamas Google Drive.

### 2. Pastraipų duomenų įkėlimas

- Nurodomas `book_code` (pvz., `'2852'`).
- Nuskaitomas ankstesniame notebook'e sukurtas failas:
  ```
  Book_Info/Vol2/book_text/df_paragraphs_<book_code>.tsv
  ```
- Šis `df_paragraphs` yra pagrindinis teksto šaltinis visai tolimesnei analizei.

### 3. spaCy modelio inicializavimas

```python
nlp = spacy.load("en_core_web_sm")
```

Šis modelis suteikia:
- Tokenizavimą (teksto skaidymą į žodžius)
- POS žymėjimą (daiktavardis, veiksmažodis ir t.t.)
- Priklausomybių analizę (sintaksinė medžio struktūra)
- Entiteto atpažinimą (NER)
- Daiktavardinių frazių išskyrimą

### 4. WordNet papildymo funkcija

`wordnet_info(word, word_pos, sentence_str)` funkcija kiekvienam tokenui grąžina tris dalykus:

**a) Dažniausiai sutinkamas sinonimų rinkinys (most frequent synset)**
Tiesiog pirmasis WordNet synset — tai statistiškai dažniausia žodžio reikšmė.

**b) Lesk algoritmo synset**
Lesk algoritmas parenka reikšmę pagal kontekstą: lygina žodžius sakinyje su WordNet apibrėžimais ir parenka labiausiai sutampantį. Tai paprasčiausias žodžių reikšmių dviprasmiškumo sprendimas (WSD — Word Sense Disambiguation).

**c) Hiponiminė grandinė (hypernym path)**
Hierarchinė grandinė nuo konkretaus žodžio iki pačios bendriausios sąvokos (pvz.: `dog → canine → carnivore → animal → organism → entity`). Tai leidžia suprasti žodžio semantinę kategoriją.

### 5. Pagrindinis anotavimo ciklas

Tai centrinė ir ilgiausia dalis. Ciklas eina per kiekvieną pastraipą iš `df_paragraphs`:

```
Kiekviena pastraipa → spaCy doc objektas
    → Kiekvienas sakinys
        → Kiekvienas tokenas
            - Surenkama: text, lemma, POS, tag, dep, head, ent_type
            - Skaičiuojamas token_id_in_sent (pozicija sakinyje)
            - Stebimas citatos būsenos perjungimas (is_quote flip-flop)
            - Kviečiama wordnet_info() → mf_synset, lesk_synset
            - Tikrinama, ar tokenas priklauso daiktavardinei frazei (token_in_chunk)
        → Kiekvienas entitetas → į entity sąrašus
        → Kiekviena daiktavardinė frazė → į noun_chunk sąrašus
```

**Citatos būsenos sekimas** (`is_quote`): kintamasis veikia kaip flip-flop — kai spaCy randa citatos simbolį (`token.is_quote == True`), reikšmė keičiasi 0→1 arba 1→0. Taip žinoma, ar tokenas priklauso personažo kalbai.

**Daiktavardinės frazės priklausomybė** (`token_in_chunk`): kiekvienam tokenui tikrinama, ar jis priklauso bent vienai noun chunk — tai papildomas požymis semantinei analizei.

### 6. DataFrame'ų sukūrimas

Iš surinktų sąrašų sukuriami trys pandas lentelės:

**`df_book_token_spacy`** — tokenų lentelė su stulpeliais:
`token`, `lemma`, `pos`, `tag`, `dep`, `is_stop`, `head`, `head_i`, `head_pos`, `ent_type`, `token_in_chunk`, `chapter`, `paragraph`, `paragraph_token_id`, `paragraph_token_strpoz`, `paragraph_sentence_id`, `token_id_in_sent`, `is_quote`, `wn_mf_synset`, `wn_lesk_synset`

**`df_book_entity_spacy`** — entitetų lentelė su stulpeliais:
`entity`, `label`, `chapter`, `paragraph`, `paragraph_entity_start`, `paragraph_entity_end`, `sent_id`

**`df_book_noun_chunk_spacy`** — frazių lentelė su stulpeliais:
`chunk`, `chapter`, `paragraph`, `paragraph_sentence_id`, `chunk_start`, `chunk_end`, `root`, `chunk_root_i`, `noun_chunk_entity`

### 7. Išsaugojimas

```python
df_book_token_spacy.to_csv('Book_Info/Vol2/tmp/df_book_token_spacy_<book_code>.tsv', sep='\t')
```

Entitetų ir frazių lentelės šiuo metu komentuotos (galima atkomentavus išsaugoti atskirai).

### 8. Interaktyvus tyrinėjimas su PyGWalker (pasirinktinai)

Notebook'as turi tris komentuotas PyGWalker sekcijas vizualinei analizei:
- Tokenų lentelė — žodžių skaičiai pagal skyrių ir citatos būseną
- Entitetų lentelė — dažniausiai pasikartojantys vardai ir jų tipai
- Frazių lentelė — dažniausios daiktavardinių frazių šaknys

### 9. Gutenberg katalogo gavimas (pasirinktinai)

Paskutinis blokas (`get_catalog = False`) leidžia parsisiųsti visą anglų knygų katalogą iš Gutenberg — naudinga naujų knygų paieškai.

---

## Svarbūs techniniai aspektai

| Aspektas | Paaiškinimas |
|---|---|
| `en_core_web_sm` | Mažas, greitas modelis — tinka produkcijai, bet mažiau tikslus nei `en_core_web_lg` |
| Lesk WSD | Paprastas, bet lėtas — kviečiamas kiekvienam ne stop-word tokenui |
| `chunk_start/end` | Pozicijos skaičiuojamos **sakinies atžvilgiu**, ne pastraipas, todėl suderinamos su `token_id_in_sent` |
| WordNet POS atitikimas | Tik NOUN, VERB, ADJ, ADV žodžiai tikrinami WordNet — kiti tokenai grąžina tuščias reikšmes |

---

## Ryšys su kitais notebook'ais

```
BookNLP.ipynb
    └──→ BookNLP_spaCy.ipynb  ← šis notebook'as
              │
              └──→ BookNLP_StableDiffusion.ipynb (naudoja df_book_token_spacy duomenis prompts generavimui)
```
