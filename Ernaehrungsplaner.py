import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Ernährungsplan Pro", page_icon="🥗", layout="wide")
st.title("🥗 Ernährungsplan Generator PRO")

# ========== SIDEBAR: PROFIL ==========
st.sidebar.header("👤 Profil")

geschlecht = st.sidebar.selectbox("Geschlecht", ["Männlich", "Weiblich"])
alter = st.sidebar.number_input("Alter", 14, 100, 30)
gewicht = st.sidebar.number_input("Gewicht (kg)", 40, 200, 75)
groesse = st.sidebar.number_input("Größe (cm)", 140, 220, 175)

aktivitaet = st.sidebar.selectbox(
    "Aktivitätslevel",
    ["Wenig Bewegung", "Leicht aktiv", "Mittel aktiv", "Sehr aktiv"]
)

ziel = st.sidebar.selectbox("Ziel", ["Abnehmen", "Gewicht halten", "Zunehmen"])
ernaehrung = st.sidebar.selectbox("Ernährungsform", ["Normal", "Vegan"])
mahlzeiten = st.sidebar.slider("Mahlzeiten pro Tag", 3, 6, 4)

# ========== KALORIENBERECHNUNG ==========
faktoren = {
    "Wenig Bewegung": 1.2,
    "Leicht aktiv": 1.375,
    "Mittel aktiv": 1.55,
    "Sehr aktiv": 1.725
}

if geschlecht == "Männlich":
    bmr = 10 * gewicht + 6.25 * groesse - 5 * alter + 5
else:
    bmr = 10 * gewicht + 6.25 * groesse - 5 * alter - 161

kalorien = int(bmr * faktoren[aktivitaet])

if ziel == "Abnehmen":
    kalorien -= 500
elif ziel == "Zunehmen":
    kalorien += 300

# ========== MAKROS ==========
protein = int((kalorien * 0.3) / 4)
carbs = int((kalorien * 0.45) / 4)
fat = int((kalorien * 0.25) / 9)

# ========== ESSENSDATEN ==========
foods = {
    "Normal": {
        "Frühstück": [
            {"name": "Haferflocken mit Beeren", "kcal": 450, "p": 20, "c": 60, "f": 12, "desc": "Perfekt für Energie"},
            {"name": "Rührei mit Vollkornbrot", "kcal": 500, "p": 30, "c": 35, "f": 22, "desc": "Proteinreich & sättigend"}
        ],
        "Mittag": [
            {"name": "Hähnchen mit Reis", "kcal": 650, "p": 45, "c": 70, "f": 12, "desc": "Ideal für Muskelaufbau"},
            {"name": "Lachs mit Kartoffeln", "kcal": 700, "p": 40, "c": 50, "f": 30, "desc": "Omega-3 Quelle"}
        ],
        "Abend": [
            {"name": "Omelette mit Gemüse", "kcal": 480, "p": 35, "c": 15, "f": 28, "desc": "Low-Carb Abendessen"},
            {"name": "Salat mit Feta", "kcal": 500, "p": 25, "c": 30, "f": 25, "desc": "Leicht & gesund"}
        ],
        "Snack": [
            {"name": "Apfel", "kcal": 95, "p": 0, "c": 25, "f": 0, "desc": "Erfrischend"},
            {"name": "Nüsse", "kcal": 180, "p": 6, "c": 8, "f": 15, "desc": "Gesunde Fette"}
        ]
    },

    "Vegan": {
        "Frühstück": [
            {"name": "Porridge mit Mandelmilch", "kcal": 420, "p": 15, "c": 60, "f": 10, "desc": "Ballaststoffreich"},
            {"name": "Smoothie Bowl", "kcal": 400, "p": 12, "c": 55, "f": 12, "desc": "Vitamine pur"}
        ],
        "Mittag": [
            {"name": "Kichererbsen-Curry", "kcal": 650, "p": 22, "c": 75, "f": 18, "desc": "Pflanzliches Protein"},
            {"name": "Tofu mit Reis", "kcal": 600, "p": 30, "c": 65, "f": 20, "desc": "Perfekt für Sport"}
        ],
        "Abend": [
            {"name": "Avocado-Salat", "kcal": 480, "p": 10, "c": 30, "f": 30, "desc": "Gesunde Fette"},
            {"name": "Vegane Suppe", "kcal": 420, "p": 15, "c": 40, "f": 18, "desc": "Leicht & warm"}
        ],
        "Snack": [
            {"name": "Hummus mit Gemüse", "kcal": 200, "p": 8, "c": 20, "f": 10, "desc": "Ideal zwischendurch"},
            {"name": "Nüsse", "kcal": 180, "p": 6, "c": 8, "f": 15, "desc": "Energiequelle"}
        ]
    }
}

# ========== PLAN GENERIEREN ==========
if st.button("📅 Wochenplan erstellen"):

    st.subheader("🔥 Tagesbedarf")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Kalorien", f"{kalorien} kcal")
    c2.metric("Protein", f"{protein} g")
    c3.metric("Kohlenhydrate", f"{carbs} g")
    c4.metric("Fett", f"{fat} g")

    plan = {}
    einkauf = []

    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    for tag in tage:
        meals = []

        meals.append(random.choice(foods[ernaehrung]["Frühstück"]))
        meals.append(random.choice(foods[ernaehrung]["Mittag"]))
        meals.append(random.choice(foods[ernaehrung]["Abend"]))

        while len(meals) < mahlzeiten:
            meals.append(random.choice(foods[ernaehrung]["Snack"]))

        plan[tag] = [m["name"] for m in meals]
        einkauf.extend([m["name"] for m in meals])

        with st.expander(f"🍽️ {tag}"):
            for m in meals:
                st.markdown(
                    f"**{m['name']}**  \n"
                    f"_{m['desc']}_  \n"
                    f"🔥 {m['kcal']} kcal | 🥩 {m['p']}g | 🍞 {m['c']}g | 🧈 {m['f']}g"
                )

    df = pd.DataFrame.from_dict(plan, orient="index")
    df.columns = [f"Mahlzeit {i+1}" for i in range(mahlzeiten)]

    st.subheader("📋 Wochenübersicht")
    st.dataframe(df)

    st.subheader("🛒 Einkaufsliste")
    einkauf_df = pd.DataFrame(sorted(set(einkauf)), columns=["Lebensmittel"])
    st.dataframe(einkauf_df)

    st.success("✅ Fertig! Dein kompletter Ernährungsplan ist erstellt.")

st.caption("⚠️ Keine medizinische Beratung – nur zur Orientierung")
