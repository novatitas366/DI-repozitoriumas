# BookNLP.ipynb — Knygos teksto paruošimas NLP analizei

## Apžvalga

Šis notebook'as yra **pirmasis iš trijų** susijusių notebook'ų grandinėje. Jo tikslas — paimti neapdorotą knygos tekstą iš Project Gutenberg (arba kito šaltinio) ir paversti jį struktūruotais duomenimis, tinkamais tolimesnei kalbos analizei.

---

## Kas gaunama po vykdymo

| Rezultatas | Aprašymas |
|---|---|
| `df_paragraphs` | Lentelė, kur kiekviena eilutė — vienas pastraipa su skyriaus numeriu ir dialogo žyma |
| `df_chapters_info` | Skyrių metaduomenys (numeris, pavadinimas, žodžių skaičius) |
| `df_paragraphs_<book_code>.tsv` | Eksportuotas failas Google Drive, perduodamas kitiems notebook'ams |

---

## Darbo eiga žingsnis po žingsnio

### 1. Konfigūracija ir aplinkos paruošimas

- Nustatomas `Vol` — aplanko pavadinimas Google Drive (pvz., `'Vol2'`).
- Montuojamas Google Drive.
- Iš GitHub nuskaitomas `file_path_dic.json` — žodynas su knygų metadata (keliai, skyrių regex'ai ir t.t.).
- Jei Drive jau yra lokalus šio žodyno kopiją, ji sujungiama su GitHub versija, kad išliktų vietiniai papildymai.

### 2. Aplankų struktūros sukūrimas

Automatiškai sukuriamas aplankynas Google Drive:

```
Book_Info/
  Vol2/
    book_text/       ← pagrindiniai TSV failai
    book_words/
    gpt4_scene_info/
    ollama_scene_info/
    cyborg_scene_info/
    tmp/
      stanza/
      wordnet/
      webots/
      masked/
```

### 3. Knygos pasirinkimas

- Nurodomas `book_name` ir `book_code` (pvz., Gutenberg ID `"2852"` = *The Hound of the Baskervilles*).
- Aprašomas `chapter_regex` — reguliarioji išraiška, pagal kurią atpažįstamos skyriaus antraštės (pvz., `r'Chapter (\d+)\.'`).
- Neprivalomi parametrai: `start_line`, `end_line`, `stringReplaceDic` (teksto korekcijoms).
- Sukuriamas atvirkštinis žodynas `book_code → book_name` ir išsaugomas Drive.

### 4. Teksto įkėlimas ir skaidymas į pastraipas

Dvi funkcijos tvarko teksto įkėlimą:

- **`get_book_good_lines_just_test`** — naudojama testiniam režimui; nuskaito tik fragmentą tarp `start_line` ir `end_line` žymų (Gutenberg failuose tai `*** START OF THE PROJECT GUTENBERG ***`).
- **`get_book_good_lines`** — nuskaito visą failą be apribojimų.

Po įkėlimo `get_book_paragraph_lines` sujungia eilutes į pastraipas (kol pastraipa nepasiekia ~400 žodžių limito — tai svarbu, nes BERT modeliai turi 512 tokenų limitą).

### 5. Skyrių atpažinimas

Funkcija `get_book_paragraphs_df` eina per visas pastraipas ir tikrina, ar eilutė atitinka `chapter_regex`. Jei taip — ji įrašoma į `df_chapters_info` kaip skyriaus antraštė. Kitos eilutės patenka į `df_paragraphs`.

### 6. Žodžių skaičiavimas pagal skyrius

`df_paragraphs` duomenys agreguojami pagal skyrių, suskaičiuojamas bendras žodžių kiekis kiekviename skyriuje ir pridedamas prie `df_chapters_info`.

### 7. Dialogo žymėjimas

Tai viena svarbiausių dalių. Sistema skiria tiesioginę kalbą nuo naratyvo:

- **`replace_quotes`** — normalizuoja kabutes (paprasti `"` → `"` / `"`).
- **`get_list_speech_or_not`** — pagal reguliariąją išraišką skaido pastraipą į segmentus, kiekvienam priskiria `is_speech = 1` (dialogas) arba `0` (naratyvas).
- **`get_splitted_speech_narrative`** — eina per visą `df_paragraphs` ir:
  - Jei pastraipa turi ir dialogą, ir naratyvą — žymi `is_speech = 2` ir ją išskaido.
  - Jei tik dialogas — `is_speech = 1`.
  - Jei tik naratyvas — `is_speech = 0`.

### 8. Išsaugojimas

Galutinis `df_paragraphs` eksportuojamas kaip TSV failas į:
```
/content/drive/MyDrive/Book_Info/Vol2/book_text/df_paragraphs_<book_code>.tsv
```

---

## Ryšys su kitais notebook'ais

```
BookNLP.ipynb
    │
    ├──→ BookNLP_spaCy.ipynb     (naudoja spaCy lingvistinei analizei)
    └──→ BookNLP_stanza.ipynb    (naudoja Stanza lingvistinei analizei)
```

Abu tolimesni notebook'ai naudoja tą patį TSV failą, todėl jų rezultatai yra tiesiogiai palyginami.

---

## Svarbūs parametrai

| Parametras | Reikšmė |
|---|---|
| `book_code` | Gutenberg ID arba lokalaus failo identifikatorius |
| `chapter_regex` | Regex skyrių antraštėms atpažinti — **būtina teisingai nustatyti kiekvienai knygai atskirai** |
| `just_test` | `True` — greitas testas su *Hound of the Baskervilles*; `False` — pilnas režimas |
| `file_encoding_scheme` | Failo koduotė (dažniausiai `utf-8` arba `windows-1252`) |
| `stringReplaceDic` | Pasirinktiniai teksto keitimai prieš apdorojimą (pvz., kabutės korekcijos) |
