# PR2 Roboto Valdiklis — Aprašymas

## Apžvalga

Šis valdiklis valdo **PR2** robotą simuliacijoje (Webots). Roboto užduotis — **perkelti objektus tarp dviejų stalų** begaliniame cikle.

---

## Roboto Struktūra

### Ratai
PR2 turi **4 caster** ratų mazgus, kiekvienas su 2 ratais (iš viso 8 ratai):
- `FLL`, `FLR` — priekinis kairysis mazgas
- `FRL`, `FRR` — priekinis dešinysis mazgas
- `BLL`, `BLR` — galinis kairysis mazgas
- `BRL`, `BRR` — galinis dešinysis mazgas

Kiekvienas mazgas turi ir **sukimosi motorą** (rotation joint), leidžiantį keisti rato kryptį.

### Rankos
Robotas turi **dvi rankas** (kairę ir dešinę), kiekviena su 5 sąnariais:
| Sąnarys | Aprašymas |
|---|---|
| `SHOULDER_ROLL` | Peties pasukimas |
| `SHOULDER_LIFT` | Peties kėlimas |
| `UPPER_ARM_ROLL` | Viršutinės rankos sukimas |
| `ELBOW_LIFT` | Alkūnės lenkimas |
| `WRIST_ROLL` | Riešo sukimas |

### Kiti įrenginiai
- **Gripper'iai** — pirštų motorai objektų griebimui
- **Torso** — liemens kėlimo/leidimo motorai
- **Kontaktiniai sensoriai** — ant pirštų galų (gripo aptikimui)
- **Kameros** — stereo, HD, ir priekiniai fotoaparatai (šioje simuliacijoje nenaudojami)
- **Lazeriniai sensoriai** — `laser_tilt` ir `base_laser` (nenaudojami)
- **IMU** — inercinių matavimų blokas (nenaudojamas)

---

## Programos Eiga

### 1. Inicijavimas
```
wb_robot_init()
  → initialize_devices()   // Gauna visų įrenginių rodykles
  → enable_devices()       // Įjungia sensoriaus apklausą
  → set_initial_position() // Nustato pradinę poziciją
```

**Pradinė pozicija:**
- Abi rankos sulenktos
- Abu gripper'iai atidaryti
- Torso pakeltas į `0.2 m`

### 2. Pasiruošimas
- Rankos nustatomas į darbinę poziciją (`elbow_lift = -0.5`)
- Robotas privažiuoja **0.35 m pirmyn** prie stalo

### 3. Pagrindinis Ciklas

```
while (true) {
  1. Uždaro abu gripper'ius (su jėgos grįžtamuoju ryšiu)
  2. Pakelia rankas aukštyn (elbow_lift = -1.0)
  3. Važiuoja atgal 0.35 m
  4. Apsisuka 180° (M_PI)
  5. Važiuoja pirmyn 0.35 m
  6. Nuleidžia rankas žemyn (elbow_lift = -0.5)
  7. Atidaro abu gripper'ius
  8. Kartoja...
}
```

---

## Svarbios Funkcijos

| Funkcija | Parametrai | Aprašymas |
|---|---|---|
| `robot_go_forward(distance)` | `distance` [m] | Važiuoja pirmyn (teigiamas) arba atgal (neigiamas) |
| `robot_rotate(angle)` | `angle` [rad] | Apsisuka nurodytu kampu |
| `set_gripper(left, open, torque, wait)` | — | Atidaro/uždaro gripper'į |
| `set_right_arm_position(...)` | 5 kampai + wait | Nustato dešinės rankos poziciją |
| `set_left_arm_position(...)` | 5 kampai + wait | Nustato kairės rankos poziciją |
| `set_torso_height(height, wait)` | `height` [m] | Keičia torso aukštį |
| `set_rotation_wheels_angles(...)` | 4 kampai + wait | Nustato ratų sukimosi kryptį |

---

## Greičio Valdymas

Robotas naudoja **dviejų greičių** sistemą:

```c
#define MAX_WHEEL_SPEED 3.0  // rad/s — maksimalus greitis

// Lėtinimas prieš tikslą:
if (fabs(distance) - wheel0_travel_distance < 0.025)
    set_wheels_speed(0.1 * max_wheel_speed);  // 10% greičio
```

Kai lieka mažiau nei **2.5 cm** iki tikslo — greitis sumažinamas iki 10%, kad sustotų tiksliai.

---

## Konstantos

| Konstanta | Reikšmė | Aprašymas |
|---|---|---|
| `TIME_STEP` | 16 ms | Simuliacijos žingsnio trukmė |
| `MAX_WHEEL_SPEED` | 3.0 rad/s | Maksimalus rato greitis |
| `WHEELS_DISTANCE` | 0.4492 m | Atstumas tarp ratų mazgų |
| `WHEEL_RADIUS` | 0.08 m | Rato spindulys |
| `TOLERANCE` | 0.05 | Paklaida pozicijos palyginimui |

---

## Sukimosi Mechanizmas

Sukantis robotas naudoja **įstrižinį ratų išdėstymą**:
```c
set_rotation_wheels_angles(
    3/4 * π,   // FL — 135°
    1/4 * π,   // FR — 45°
   -3/4 * π,   // BL — -135°
   -1/4 * π    // BR — -45°
);
```
Tai leidžia robotui suktis **aplink savo centrą** (tank-turn).

---

*Dokumentas sugeneruotas pagal Webots PR2 valdiklio šaltinio kodą.*
