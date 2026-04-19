"""
Studento egzamino Bajeso tinklas naudojant pgmpy.
Tinklo struktūra pagal Student_Exam_BN.json.

Kintamieji (reikšmės: 1 = taip, 0 = ne):
  Motyvacija  – studentas motyvuotas
  Vakarelis   – studentas buvo vakarėlyje prieš egzaminą
  Mokesi      – studentas mokėsi
  Issimiegojo – studentas išsimiegojo
  Egzaminas   – studentas išlaikė egzaminą
  Stipendija  – studentas gaus stipendiją
"""

from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

# ---------------------------------------------------------------------------
# 1. Tinklo struktūra (briaunos)
# ---------------------------------------------------------------------------
model = BayesianNetwork([
    ("Motyvacija",  "Mokesi"),
    ("Vakarelis",   "Mokesi"),
    ("Vakarelis",   "Issimiegojo"),
    ("Mokesi",      "Egzaminas"),
    ("Issimiegojo", "Egzaminas"),
    ("Egzaminas",   "Stipendija"),
])

# ---------------------------------------------------------------------------
# 2. Sąlyginės tikimybių lentelės (CPT)
#    Reikšmių tvarka: [1, 0]  (1 = taip, 0 = ne)
# ---------------------------------------------------------------------------

# Motyvacija – šaknis
cpd_motyvacija = TabularCPD(
    variable="Motyvacija",
    variable_card=2,
    values=[[0.6],   # P(Mot=1)
            [0.4]],  # P(Mot=0)
    state_names={"Motyvacija": [1, 0]},
)

# Vakarelis – šaknis
cpd_vakarelis = TabularCPD(
    variable="Vakarelis",
    variable_card=2,
    values=[[0.3],   # P(Vak=1)
            [0.7]],  # P(Vak=0)
    state_names={"Vakarelis": [1, 0]},
)

# Issimiegojo | Vakarelis
# Stulpelių tvarka: Vak=1, Vak=0
cpd_issimiegojo = TabularCPD(
    variable="Issimiegojo",
    variable_card=2,
    values=[[0.2, 0.9],   # P(Iss=1 | Vak)
            [0.8, 0.1]],  # P(Iss=0 | Vak)
    evidence=["Vakarelis"],
    evidence_card=[2],
    state_names={"Issimiegojo": [1, 0], "Vakarelis": [1, 0]},
)

# Mokesi | Motyvacija, Vakarelis
# Stulpelių tvarka (lėčiausiai kinta pirmas tėvas):
#   Mot=1,Vak=1 | Mot=1,Vak=0 | Mot=0,Vak=1 | Mot=0,Vak=0
cpd_mokesi = TabularCPD(
    variable="Mokesi",
    variable_card=2,
    values=[[0.50, 0.95, 0.10, 0.40],   # P(Mok=1 | ...)
            [0.50, 0.05, 0.90, 0.60]],  # P(Mok=0 | ...)
    evidence=["Motyvacija", "Vakarelis"],
    evidence_card=[2, 2],
    state_names={"Mokesi": [1, 0], "Motyvacija": [1, 0], "Vakarelis": [1, 0]},
)

# Egzaminas | Mokesi, Issimiegojo
# Stulpelių tvarka:
#   Mok=1,Iss=1 | Mok=1,Iss=0 | Mok=0,Iss=1 | Mok=0,Iss=0
cpd_egzaminas = TabularCPD(
    variable="Egzaminas",
    variable_card=2,
    values=[[0.95, 0.75, 0.50, 0.15],   # P(Egz=1 | ...)
            [0.05, 0.25, 0.50, 0.85]],  # P(Egz=0 | ...)
    evidence=["Mokesi", "Issimiegojo"],
    evidence_card=[2, 2],
    state_names={"Egzaminas": [1, 0], "Mokesi": [1, 0], "Issimiegojo": [1, 0]},
)

# Stipendija | Egzaminas
# Stulpelių tvarka: Egz=1, Egz=0
cpd_stipendija = TabularCPD(
    variable="Stipendija",
    variable_card=2,
    values=[[0.85, 0.05],   # P(Stip=1 | Egz)
            [0.15, 0.95]],  # P(Stip=0 | Egz)
    evidence=["Egzaminas"],
    evidence_card=[2],
    state_names={"Stipendija": [1, 0], "Egzaminas": [1, 0]},
)

# ---------------------------------------------------------------------------
# 3. CPT pridėjimas ir validacija
# ---------------------------------------------------------------------------
model.add_cpds(
    cpd_motyvacija, cpd_vakarelis, cpd_issimiegojo,
    cpd_mokesi, cpd_egzaminas, cpd_stipendija,
)

print("=" * 55)
print("Modelio validacija:", model.check_model())
print("Mazgai:", model.nodes())
print("Briaunos:", model.edges())

# ---------------------------------------------------------------------------
# 4. Tikimybių užklausos (Variable Elimination)
# ---------------------------------------------------------------------------
ve = VariableElimination(model)

print("\n" + "=" * 55)
print("TIKIMYBIŲ UŽKLAUSOS")
print("=" * 55)

# --- Nesąlyginės tikimybės ---
for var in ["Motyvacija", "Vakarelis", "Mokesi", "Issimiegojo", "Egzaminas", "Stipendija"]:
    r = ve.query([var])
    p1 = r.values[0]   # reikšmė 1
    p0 = r.values[1]   # reikšmė 0
    print(f"\nP({var}=1) = {p1:.4f}   P({var}=0) = {p0:.4f}")

# --- Sąlyginės tikimybės ---
print("\n" + "-" * 55)
queries = [
    # (kintamasis, įrodymai, aprašymas)
    ("Egzaminas",  {"Motyvacija": 1, "Vakarelis": 0},
     "P(Egzaminas | Motyvacija=1, Vakarelis=0)"),
    ("Egzaminas",  {"Motyvacija": 0, "Vakarelis": 1},
     "P(Egzaminas | Motyvacija=0, Vakarelis=1)"),
    ("Stipendija", {"Egzaminas": 1},
     "P(Stipendija | Egzaminas=1)"),
    ("Stipendija", {"Egzaminas": 0},
     "P(Stipendija | Egzaminas=0)"),
    ("Mokesi",     {"Motyvacija": 1},
     "P(Mokesi | Motyvacija=1)"),
    ("Egzaminas",  {"Mokesi": 1, "Issimiegojo": 1},
     "P(Egzaminas | Mokesi=1, Issimiegojo=1)"),
    ("Egzaminas",  {"Mokesi": 0, "Issimiegojo": 0},
     "P(Egzaminas | Mokesi=0, Issimiegojo=0)"),
]

for var, evidence, label in queries:
    r = ve.query([var], evidence=evidence)
    p1 = r.values[0]
    p0 = r.values[1]
    print(f"\n{label}")
    print(f"  P(=1) = {p1:.4f}   P(=0) = {p0:.4f}")

# ---------------------------------------------------------------------------
# 5. Grafinis atvaizdavimas
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 7))

pos = {
    "Motyvacija":  (0.5, 4.0),
    "Vakarelis":   (3.5, 4.0),
    "Mokesi":      (0.5, 2.5),
    "Issimiegojo": (3.5, 2.5),
    "Egzaminas":   (2.0, 1.0),
    "Stipendija":  (2.0, -0.5),
}

node_colors = {
    "Motyvacija":  "#AED6F1",
    "Vakarelis":   "#A9DFBF",
    "Mokesi":      "#AED6F1",
    "Issimiegojo": "#A9DFBF",
    "Egzaminas":   "#F9E79F",
    "Stipendija":  "#F1948A",
}

nx.draw_networkx_nodes(
    model, pos=pos, ax=ax,
    node_size=4000,
    node_color=[node_colors[n] for n in model.nodes()],
)
nx.draw_networkx_labels(model, pos=pos, ax=ax, font_size=10, font_weight="bold")
nx.draw_networkx_edges(
    model, pos=pos, ax=ax,
    arrows=True, arrowsize=25, arrowstyle="-|>",
    width=2, edge_color="#555555",
    connectionstyle="arc3,rad=0.05",
    min_source_margin=30, min_target_margin=30,
)

ax.set_title("Studento egzamino Bajeso tinklas", fontsize=14, pad=15)
ax.axis("off")
plt.tight_layout()
plt.savefig("bajeso_tinklas.png", dpi=150)
print("\n\nGrafas išsaugotas: bajeso_tinklas.png")
