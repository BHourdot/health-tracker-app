import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Santé Connectée", page_icon="🏥")

# --- FONCTION POUR GÉNÉRER LE CSS DYNAMIQUE ---
def apply_custom_slider_style(value_douleur, value_fatigue):
    # Palette de 1 (Vert) à 10 (Rouge)
    colors = {
        1: "#22c55e", 2: "#4ade80", 3: "#84cc16", 4: "#a8d810", 
        5: "#eab308", 6: "#f59e0b", 7: "#f97316", 8: "#ea580c", 
        9: "#dc2626", 10: "#b91d1d"
    }
    
    color_d = colors.get(value_douleur, "#2563eb")
    color_f = colors.get(value_fatigue, "#2563eb")

    # CSS pour cibler le bouton circulaire (thumb) des sliders
    st.markdown(f"""
        <style>
        /* Cible tous les curseurs de la page */
        div[role="slider"] {{
            background-color: transparent !important; 
            border: none !important;
        }}
        
        /* Modifie la couleur de la poignée du slider */
        input[type="range"]::-webkit-slider-thumb {{
            background: {color_d} !important;
        }}
        
        /* Version spécifique pour Streamlit (Widget Thumb) */
        .stSlider [data-baseweb="slider"] div[role="slider"] {{
            background-color: {color_d} !important;
            box-shadow: 0 0 10px {color_d}55;
            border: 2px solid white !important;
            height: 25px !important;
            width: 25px !important;
        }}
        
        /* Pour différencier si besoin, mais Streamlit applique souvent le dernier style lu 
           aux deux. Ici on applique une couleur moyenne ou celle du dernier actif */
        </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES ÉTATS ---
if 'douleur' not in st.session_state: st.session_state.douleur = 1
if 'fatigue' not in st.session_state: st.session_state.fatigue = 5

st.title("🏥 Suivi d'État de Forme")

# --- FORMULAIRE ---
with st.form("health_form"):
    
    st.write("### 1. Évaluation de la Douleur (1-10)")
    douleur = st.select_slider(
        "Intensité de la douleur :",
        options=list(range(1, 11)),
        key="slider_douleur"
    )
    
    st.divider()

    st.write("### 2. Bien-être Mental (WHO-5)")
    options_be = {
        "Tout le temps": 5, "La plupart du temps": 4, 
        "Plus de la moitié du temps": 3, "Moins de la moitié du temps": 2, 
        "De temps en temps": 1, "Jamais": 0
    }
    choix_psy = st.radio("Au cours des 2 dernières semaines, je me suis senti(e) gai(e) et de bonne humeur :", 
                         options=list(options_be.keys()), horizontal=True)

    st.divider()

    st.write("### 3. Niveau de Fatigue (1-10)")
    fatigue = st.slider("Intensité de la fatigue :", 1, 10, 5, key="slider_fatigue")

    submitted = st.form_submit_button("Enregistrer les résultats")

# Application du style basé sur les valeurs sélectionnées
apply_custom_slider_style(douleur, fatigue)

# --- AFFICHAGE DU RÉSULTAT ---
if submitted:
    st.balloons()
    st.success(f"Données prêtes : Douleur {douleur}/10, Fatigue {fatigue}/10")
    # Logique de connexion Cloud ici...
