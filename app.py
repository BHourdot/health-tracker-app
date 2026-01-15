import streamlit as st
import pandas as pd
import datetime

# Configuration
st.set_page_config(page_title="Suivi de Forme", page_icon="🏥")

# --- FONCTION DE COULEUR ---
def get_visual_indicator(value):
    # Dégradé du vert au rouge
    colors = ["#22c55e", "#4ade80", "#84cc16", "#a8d810", "#eab308", "#f59e0b", "#f97316", "#ea580c", "#dc2626", "#b91d1d"]
    color = colors[value-1]
    
    # Barre de progression colorée personnalisée
    html = f"""
    <div style="background-color: #e2e8f0; border-radius: 10px; width: 100%; height: 12px; margin-top: 10px;">
        <div style="background-color: {color}; width: {value*10}%; height: 12px; border-radius: 10px; transition: width 0.3s ease;"></div>
    </div>
    <div style="color: {color}; font-weight: bold; font-size: 20px; margin-top: 5px;">
        Score : {value} / 10
    </div>
    """
    return html

st.title("🏥 Suivi d'État de Forme")
st.info("Déplacez les curseurs pour voir l'indicateur de couleur changer en temps réel.")

# --- QUESTIONS (HORS FORMULAIRE POUR LE TEMPS RÉEL) ---

# 1. DOULEUR
st.write("### 1. Évaluation de la Douleur")
douleur = st.select_slider(
    "1 = Très faible | 10 = Insupportable",
    options=list(range(1, 11)),
    key="slider_d"
)
st.markdown(get_visual_indicator(douleur), unsafe_allow_html=True)

st.divider()

# 2. BIEN-ÊTRE
st.write("### 2. Bien-être Mental")
options_be = {"Tout le temps": 5, "La plupart du temps": 4, "Plus de la moitié du temps": 3, "Moins de la moitié du temps": 2, "De temps en temps": 1, "Jamais": 0}
choix_psy = st.radio("Sensation de gaieté au cours des 2 dernières semaines :", options=list(options_be.keys()), horizontal=True)

st.divider()

# 3. FATIGUE
st.write("### 3. Niveau de Fatigue")
fatigue = st.select_slider(
    "1 = Forme olympique | 10 = Épuisement total",
    options=list(range(1, 11)),
    value=5,
    key="slider_f"
)
st.markdown(get_visual_indicator(fatigue), unsafe_allow_html=True)

st.divider()

# --- BOUTON D'ENREGISTREMENT ---
if st.button("🚀 Enregistrer les données dans le Cloud"):
    # Ici, on simule l'enregistrement
    st.balloons()
    st.success(f"Données enregistrées le {datetime.datetime.now().strftime('%d/%m/%Y')}")
    
    # Résumé pour vérification
    resultats = {
        "Douleur": douleur,
        "Bien-être (Score)": options_be[choix_psy],
        "Fatigue": fatigue
    }
    st.write("### Résumé des indicateurs :")
    st.dataframe(pd.DataFrame([resultats]))
