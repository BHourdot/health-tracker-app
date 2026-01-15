import streamlit as st
import pandas as pd
import datetime

# Configuration
st.set_page_config(page_title="Santé Connectée", page_icon="🏥", layout="centered")

# --- FONCTION DE COULEUR ---
def get_info_box(label, value):
    # Palette du vert (1) au rouge (10)
    colors = {
        1: "#22c55e", 2: "#4ade80", 3: "#84cc16", 4: "#a8d810", 
        5: "#eab308", 6: "#f59e0b", 7: "#f97316", 8: "#ea580c", 
        9: "#dc2626", 10: "#b91d1d"
    }
    color = colors.get(value, "#2563eb")
    # Retourne un badge HTML stylisé
    return f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <span style="font-weight: bold; margin-right: 10px;">{label} :</span>
        <div style="background-color:{color}; color:white; padding:5px 15px; border-radius:20px; font-weight:bold; font-size:18px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            {value} / 10
        </div>
    </div>
    """

st.title("🏥 Mon Suivi de Santé")
st.markdown("---")

# --- FORMULAIRE ---
with st.form("health_form"):
    
    # 1. DOULEUR
    st.write("### 1. Évaluation de la Douleur")
    # On place un container vide pour l'affichage dynamique
    douleur = st.select_slider(
        "Faites glisser le curseur (1 = Faible, 10 = Intense)",
        options=list(range(1, 11)),
        value=1
    )
    st.markdown(get_info_box("Niveau de douleur", douleur), unsafe_allow_html=True)
    
    st.divider()

    # 2. BIEN-ÊTRE
    st.write("### 2. Bien-être Mental")
    st.write("Au cours des 2 dernières semaines, je me suis senti(e) gai(e) et de bonne humeur :")
    options_be = {
        "Tout le temps": 5, "La plupart du temps": 4, 
        "Plus de la moitié du temps": 3, "Moins de la moitié du temps": 2, 
        "De temps en temps": 1, "Jamais": 0
    }
    choix_psy = st.radio("Sélectionnez votre ressenti :", options=list(options_be.keys()), horizontal=True)

    st.divider()

    # 3. FATIGUE
    st.write("### 3. Niveau de Fatigue")
    fatigue = st.slider("Intensité (1 = Forme olympique, 10 = Épuisement)", 1, 10, 5)
    st.markdown(get_info_box("Niveau de fatigue", fatigue), unsafe_allow_html=True)

    st.write("")
    submitted = st.form_submit_button("🚀 Enregistrer les données dans le Cloud")

# --- TRAITEMENT DES DONNÉES ---
if submitted:
    st.success("✅ Vos indicateurs ont été enregistrés avec succès.")
    
    # Préparation pour le cloud
    data_to_save = {
        "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "Douleur": douleur,
        "Bien-etre": options_be[choix_psy],
        "Fatigue": fatigue
    }
    st.json(data_to_save)
