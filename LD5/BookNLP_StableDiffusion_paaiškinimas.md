# BookNLP_StableDiffusion.ipynb — Teksto pavertimas vaizdais ir vaizdo įrašu

## Apžvalga

Šis notebook'as yra **paskutinis** grandinėje — paima knygos ar filmo scenų aprašymus ir paverčia juos vaizdais naudodamas Stable Diffusion modelį, o galų gale sujungia viską į vaizdo įrašą su garsine takelio.

---

## Kas gaunama po vykdymo

| Rezultatas | Aprašymas |
|---|---|
| `saved_images/image_N.jpg` | Kiekvienai scenai sugeneruotas vaizdas |
| `saved_images.zip` | Suarchyvuoti visi vaizdai, nukopijuoti į Google Drive |
| `output_video_with_audio.mp4` | Vaizdo įrašas: kiekvienas kadras = viena scena, garso takeliu nuskaitytas scenos aprašymas |

---

## Darbo eiga žingsnis po žingsnio

### 1. Importai ir stilių sąrašas

Pirmajame bloke importuojamos visos reikalingos bibliotekos ir apibrėžiamas `style_list` — daugiau nei 50 meninių stilių sąrašas (pvz., `"anime art style"`, `"Salvador Dali"`, `"Cyberpunk"`, `"Pixel art"`, `"Vincent van Gogh"` ir t.t.). Vienas iš jų pasirenkamas kaip aktyvus stilius visiems generuojamiems vaizdams.

### 2. Google Drive montavimas

Standartinis Google Colab Drive montavimas — reikalingas failų išsaugojimui.

### 3. Scenų aprašymų (prompt'ų) gavimas

Tai lankstiausia dalis — yra **trys būdai** gauti scenos aprašymus:

**1 būdas — tiesioginis JSON įklijavimas:**
Kintamajam `prompt_response_json_text` priskiriamas ChatGPT/Gemini sugeneruotas JSON su scenų aprašymais. Notebook'as pateikia pavyzdį su *The Matrix* pirmąja scena.

**2 būdas — prompt'o naudojimas:**
Notebook'as pateikia paruoštą prompt'ą ChatGPT tipo modeliui. Prompt'as prašo sukurti N scenų JSON formatu su atributais:
- `scene_title`, `description`, `scene_environment`
- `scene_type` (INT/EXT), `scene_date`, `location`, `time_of_day`
- `characters`, `objects`, `object_part_of_object`
- `motion_sequence`, `constant_state_sequence`
- `dialog_summary`

**3 būdas — JSON failas iš interneto:**
Jei `prompt_response_json_text` tuščias, automatiškai atsisiunčiamas jau paruoštas JSON iš GitHub repozitorijos pagal `book_code`.

Po JSON nuskaitymo iš jo ištraukiami `description`, `scene_date`, `location` ir `objects` kiekvienai scenai — jie bus naudojami kaip Stable Diffusion prompt'ai.

### 4. Stable Diffusion modelio įkėlimas (Hyper-SDXL)

```python
base_model_id = "stabilityai/stable-diffusion-xl-base-1.0"
repo_name = "ByteDance/Hyper-SD"
ckpt_name = "Hyper-SDXL-12steps-CFG-lora.safetensors"
```

Naudojamas **Hyper-SDXL** — tai SDXL modelis su LoRA svoriu iš ByteDance, optimizuotas generuoti kokybišką vaizdą vos per 8–12 žingsnių (standartinis SDXL reikalauja 25–50). Taip generavimas greitesnis neprarandant kokybės.

Modelis įkeliamas su `torch_dtype=torch.float16` (FP16 — pusė tikslumo, bet dvigubai greičiau ir mažiau VRAM) ir perkeliamas į `cuda` (NVIDIA GPU).

**TCDScheduler** — specialus triukšmo šalinimo planuotojas, suderintas su Hyper-SD greito generavimo technika.

### 5. Vaizdų generavimas

Kiekvienai scenai konstruojamas sudėtinis prompt'as iš kelių dalių:

```
"<metai>. Location is <vieta>. Objects: <objektai>. <stilius>. <scenos aprašymas>"
```

Pavyzdys: `"1999. Location is Abandoned Building. Objects: computer, monitor, keyboard. Colorful cartoon drawing style. A dark, cramped room cluttered with computers..."`

Pagrindiniai generavimo parametrai:
| Parametras | Reikšmė | Paaiškinimas |
|---|---|---|
| `num_inference_steps` | 12 | Žingsnių skaičius (mažiau = greičiau, bet mažiau detalės) |
| `guidance_scale` | 5.0–8.0 | Kiek stipriai modelis laikosi prompt'o |
| `eta` | 0.1 | Atsitiktinumo lygis (mažiau = daugiau detalių) |
| `negative_prompt` | `"distorted, ugly, deformed..."` | Ką modelis turėtų vengti |
| `seed` | atsitiktinis | Reprodukuojamumui — tas pats seed = tas pats vaizdas |

Visi sugeneruoti vaizdai saugomi `all_images_list` sąraše kaip `(nr, prompt, PIL_image)` tuple'ai.

### 6. Vaizdų išsaugojimas

- Vaizdai konvertuojami į numpy masyvus ir išsaugomi kaip `image_0.jpg`, `image_1.jpg` ir t.t.
- Sukuriamas ZIP archyvas ir nukopijuojamas į Google Drive.

### 7. Garsinio takelio generavimas (gTTS)

Kiekvienai scenai naudojant `gTTS` (Google Text-to-Speech):
- Scenos aprašymas paverčiamas garsu (`lang='en'`, `tld='co.uk'` = britų akcentas)
- Išsaugomas kaip MP3 failas

### 8. Vaizdo įrašo surinkimas (MoviePy)

Galutinis vaizdo įrašas konstruojamas taip:
1. Kiekvienam kadrui (vaizdui) priskiriamas atitinkamas garso klipas
2. Kadro trukmė = garso klipo trukmė (t.y. skirtingos scenos gali turėti skirtingą ilgį)
3. Visi klipai sujungiami nuosekliai
4. Eksportuojamas `output_video_with_audio.mp4` su H.264 kodeku

---

## Komentuotas senas kodas (sekcijos ⛔)

Notebook'e yra trys komentuotos sekcijos, pažymėtos ⛔:

| Sekcija | Kas tai |
|---|---|
| **⛔ 3. Old Code** | Senasis `keras_cv` + `tensorflow` sprendimas (pakeistas Diffusers) |
| **⛔ 4. Let's illustrate our book** | Alternatyvus metodas: prompt'ai generuojami tiesiai iš `df_book_token_spacy` (artefaktų ir personažų frazės iš spaCy) — veikė su senu Keras modeliu |
| **⛔ 5. Old video** | Senasis OpenCV + MoviePy vaizdo įrašo kūrimas be garso takelio |

Šios sekcijos parodo projekto evoliuciją — nuo Keras/KerasCV prie modernesnio Diffusers/HuggingFace ekosistemos.

---

## Priklausomybių schema

```
scenų JSON (iš ChatGPT / GitHub)
    ↓
prompt'ų surinkimas (description + date + location + objects + style)
    ↓
Hyper-SDXL (stabilityai/SDXL-base + ByteDance/Hyper-SD LoRA)
    ↓
vaizdai (PIL Image → numpy → JPG failai)
    ↓
gTTS (tekstas → MP3 garso failus)
    ↓
MoviePy (vaizdai + garsas → MP4 vaizdo įrašas)
```

---

## Ryšys su kitais notebook'ais

Šis notebook'as gali veikti **dviem režimais**:

1. **Savarankiškai** — naudojant JSON scenų aprašymus (iš ChatGPT arba GitHub). Tada `BookNLP.ipynb` ir `BookNLP_spaCy.ipynb` nereikalingi.

2. **Kaip grandinės dalis** — naudojant komentuotą ⛔ 4 sekciją, kuri remiasi `df_book_token_spacy` duomenimis iš `BookNLP_spaCy.ipynb`. Tokiu atveju prompt'ai automatiškai generuojami iš knygos turinio.

```
BookNLP.ipynb → BookNLP_spaCy.ipynb → BookNLP_StableDiffusion.ipynb
                                              ↑
                          arba tiesiogiai su ChatGPT JSON
```
