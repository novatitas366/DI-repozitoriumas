# TensorFlow pavyzdžio analizė: IMDB filmų atsiliepimų sentimento klasifikavimas

## Pavyzdžio šaltinis

Oficialus TensorFlow pavyzdys: **Basic text classification** (pagrindinė teksto klasifikacija), pritaikytas naudojant `tf.keras` ir įmontuotą IMDB duomenų rinkinį. Užduotis – binarinė klasifikacija: nustatyti, ar filmo atsiliepimas yra **teigiamas** (1), ar **neigiamas** (0).

## Duomenų rinkinys

**IMDB Reviews** – 50 000 filmų atsiliepimų iš Internet Movie Database:
- 25 000 treniravimui, 25 000 testavimui
- Kiekvienas atsiliepimas jau suindeksuotas kaip sveikųjų skaičių sąrašas (kiekvienas skaičius = žodis žodyne)
- Etiketės: `0` = neigiamas, `1` = teigiamas

## Pilnas kodas

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np

# 1. Duomenų įkėlimas
imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

# 2. Duomenų paruošimas – padding iki vienodo ilgio
train_data = keras.preprocessing.sequence.pad_sequences(
    train_data, value=0, padding='post', maxlen=256)
test_data = keras.preprocessing.sequence.pad_sequences(
    test_data, value=0, padding='post', maxlen=256)

# 3. Modelio architektūra
vocab_size = 10000
model = keras.Sequential([
    keras.layers.Embedding(vocab_size, 16),
    keras.layers.GlobalAveragePooling1D(),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# 4. Modelio kompiliavimas
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 5. Validacijos rinkinio atskyrimas
x_val = train_data[:10000]
partial_x_train = train_data[10000:]
y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

# 6. Modelio treniravimas
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=40,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)

# 7. Modelio vertinimas
results = model.evaluate(test_data, test_labels, verbose=2)
print(f"Testo nuostolis: {results[0]:.4f}")
print(f"Testo tikslumas: {results[1]:.4f}")
```

## Eilutė-po-eilutės paaiškinimas

### Bibliotekų importas

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np
```

- `tensorflow` – pagrindinė mašininio mokymosi biblioteka.
- `keras` – aukšto lygio API modelių kūrimui (įeina į TF).
- `numpy` – darbui su masyvais (TF duomenys grąžinami kaip NumPy masyvai).

### 1. Duomenų įkėlimas

```python
imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
```

- `keras.datasets.imdb` – įmontuotas IMDB duomenų rinkinys.
- `load_data(num_words=10000)` – atsisiunčia duomenis ir palieka tik **10 000 dažniausiai vartojamų žodžių**. Retesni žodžiai pašalinami, kad žodynas būtų valdomas.
- Grąžinami du tuple: treniravimo ir testavimo duomenys bei etiketės.
- `train_data` – sąrašas sąrašų, kur kiekvienas vidinis sąrašas yra sveikųjų skaičių seka (pvz., `[1, 14, 22, 16, 43, ...]`), atitinkanti vieną atsiliepimą.
- `train_labels` – masyvas `0` ir `1` reikšmių.

### 2. Duomenų paruošimas – padding

```python
train_data = keras.preprocessing.sequence.pad_sequences(
    train_data, value=0, padding='post', maxlen=256)
```

**Problema:** atsiliepimai yra skirtingo ilgio, o neuroninis tinklas reikalauja vienodo dydžio įvestis.

- `pad_sequences` – sutrumpina ilgesnes ir prailgina trumpesnes sekas.
- `value=0` – kuo užpildyti trumpesnes sekas (0 = specialus „padding" žymeklis).
- `padding='post'` – užpildo **sekos gale** (alternatyva: `'pre'` – pradžioje).
- `maxlen=256` – visi atsiliepimai bus lygiai 256 žodžių ilgio.

Tas pats atliekama su testo duomenimis – labai svarbu, kad treniravimo ir testo duomenys būtų apdoroti vienodai.

### 3. Modelio architektūra

```python
vocab_size = 10000
model = keras.Sequential([
    keras.layers.Embedding(vocab_size, 16),
    keras.layers.GlobalAveragePooling1D(),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
```

`keras.Sequential` – modelis, kur sluoksniai einami vienas po kito.

**Sluoksnis 1: `Embedding(10000, 16)`**
- Kiekvienas iš 10 000 žodynų žodžių paverčiamas **16 dimensijų tankiu vektoriumi**.
- Išvestis: tenzorius `(batch, 256, 16)` – kiekvienam iš 256 žodžių sekoje gauname 16-matį vektorių.
- Šie vektoriai treniruojami kartu su modeliu ir palaipsniui išmoksta reprezentuoti žodžių reikšmes.

**Sluoksnis 2: `GlobalAveragePooling1D()`**
- Suvidurkina visų 256 žodžių vektorius į **vieną 16-matį vektorių**.
- Išvestis: `(batch, 16)`.
- Tai paprastas būdas gauti fiksuoto dydžio atsiliepimo reprezentaciją, nepriklausomai nuo jo ilgio.

**Sluoksnis 3: `Dense(16, activation='relu')`**
- Pilnai sujungtas sluoksnis su 16 neuronų.
- `relu` (rectified linear unit): `f(x) = max(0, x)` – netiesinė aktyvacija, leidžianti modeliui mokytis sudėtingesnių priklausomybių.

**Sluoksnis 4: `Dense(1, activation='sigmoid')`**
- Vienas išvesties neuronas.
- `sigmoid`: `f(x) = 1/(1+e^-x)` – išvestį suspaudžia į intervalą `[0, 1]`, kurį interpretuojame kaip **tikimybę, kad atsiliepimas teigiamas**.

### 4. Modelio kompiliavimas

```python
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
```

- `optimizer='adam'` – Adam algoritmas svorių atnaujinimui (automatiškai pritaiko mokymosi greitį, gerai veikia daugumoje užduočių).
- `loss='binary_crossentropy'` – nuostolio funkcija binarinei klasifikacijai. Matuoja atstumą tarp prognozuotos tikimybės ir tikrosios etiketės (0 arba 1).
- `metrics=['accuracy']` – papildomai stebimas tikslumas (teisingų prognozių dalis).

### 5. Validacijos rinkinio atskyrimas

```python
x_val = train_data[:10000]
partial_x_train = train_data[10000:]
y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]
```

- Iš 25 000 treniravimo pavyzdžių pirmieji 10 000 atidedami **validacijai** (stebėti, ar modelis nepersimoko).
- Likę 15 000 naudojami faktiniam treniravimui.
- Testo duomenų neliečiame – jie bus naudojami tik gale galutiniam vertinimui.

### 6. Modelio treniravimas

```python
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=40,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)
```

- `epochs=40` – visi treniravimo duomenys bus peržiūrėti 40 kartų.
- `batch_size=512` – svoriai atnaujinami po kiekvienų 512 pavyzdžių (mini-batch gradient descent).
- `validation_data` – po kiekvienos epochos modelis vertinamas validacijos rinkinyje (bet svoriai pagal tai neatnaujinami).
- `verbose=1` – rodo progreso juostą.
- `history` – objektas, kuriame saugoma kiekvienos epochos nuostolių ir tikslumo istorija (galima vėliau atvaizduoti grafikais).

### 7. Vertinimas testo duomenimis

```python
results = model.evaluate(test_data, test_labels, verbose=2)
print(f"Testo nuostolis: {results[0]:.4f}")
print(f"Testo tikslumas: {results[1]:.4f}")
```

- `evaluate` – paleidžia modelį su testo duomenimis ir grąžina `[nuostolis, tikslumas]`.
- Testo rinkinys nebuvo matytas treniravimo metu – tai **sąžiningas** modelio kokybės įvertinimas.
- Tipinis rezultatas su šia architektūra: ~87% tikslumas.

## Pilnas duomenų srauto pavyzdys

Tarkime, vienas atsiliepimas (jau paruoštas): `[1, 14, 22, 16, 43, 0, 0, ..., 0]` (256 elementai).

1. **Embedding** → `(256, 16)` matrica – kiekvienas žodis tampa 16-mačiu vektoriumi.
2. **GlobalAveragePooling1D** → `(16,)` vektorius – vidurkis per visus žodžius.
3. **Dense(16, relu)** → `(16,)` – netiesinė transformacija.
4. **Dense(1, sigmoid)** → `(1,)`, pvz., `0.87` – 87% tikimybė, kad atsiliepimas teigiamas.

Sprendimo taisyklė: jei išvestis > 0.5, klasifikuojama kaip teigiamas; kitaip – neigiamas.

## Pagrindiniai koncepciniai dalykai

| Koncepcija | Paaiškinimas |
|------------|--------------|
| **Embedding** | Būdas paversti diskrečius tokenus (žodžius) tankiais vektoriais, kuriuos modelis gali apdoroti. |
| **Pooling** | Fiksuoto dydžio reprezentacijos gavimas iš kintamo ilgio sekos. |
| **Binarinė kryžminė entropija** | Standartinė nuostolio funkcija užduotims su dviem klasėmis. |
| **Validacijos rinkinys** | Leidžia aptikti persimokymą – kai treniravimo tikslumas auga, o validacijos krenta. |
| **Sigmoid išvestis** | Binarinės klasifikacijos tikimybinė išvestis. |

## Galimi patobulinimai

- Naudoti **LSTM** ar **1D konvoliucinius** sluoksnius vietoj pooling – jie atsižvelgtų į žodžių tvarką.
- Pridėti **Dropout** sluoksnį kovai su persimokymu.
- Naudoti **iš anksto apmokytus įterpimus** (pvz., GloVe, Word2Vec).
- Taikyti **ankstyvą sustabdymą** (`EarlyStopping` callback), kad treniravimas nutrūktų, kai validacijos nuostolis pradeda didėti.
