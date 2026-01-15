import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Configuration de la page
st.set_page_config(page_title="Santé Connectée", page_icon="🏥")

# --- FONCTION POUR LA COULEUR DYNAMIQUE ---
def get_status_circle(value):
    """Retourne une pastille colorée de 0 (vert) à 10 (rouge)"""
    colors = [
        "#22c55e", "#4ade80", "#84cc16", "#a8d810", "#eab308", 
        "#f59e0b", "#f97316", "#ea580c", "#dc2626", "#b91d1d", "#7f1d1d"
    ]
    # Sécurité pour l'index
    val = int(value) if 0 <= int(value) <= 10 else 0
    return f'<span style="height: 20px; width: 20px; background-color: {colors[val]}; border-radius: 50%; display: inline-block; margin-left: 10px; vertical-align: middle; border: 1px solid #ddd;"></span>'

# --- CONNEXION CLOUD ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    conn = None

st.title("🏥 Suivi d'État de Forme")

with st.form("health_form"):
    
    # --- 1. DOULEUR ---
    st.write("### 1. Évaluation de la Douleur (EVA)")
    douleur = st.select_slider(
        "Sélectionnez votre niveau de douleur :",
        options=list(range(11)),
        value=0
    )
    # Affichage du chiffre avec sa couleur
    st.markdown(f"**Niveau sélectionné : {douleur}** {get_status_circle(douleur)}", unsafe_allow_html=True)
    
    st.divider()

    # --- 2. BIEN-ÊTRE (WHO-5) ---
    st.write("### 2. Bien-être Mental (Indice WHO-5)")
    st.write("**Au cours des 2 dernières semaines, je me suis senti(e) gai(e) et de bonne humeur :**")
    
    # Dictionnaire pour mapper le texte au score
    options_bien_etre = {
        "Tout le temps": 5,
        "La plupart du temps": 4,
        "Plus de la moitié du temps": 3,
        "Moins de la moitié du temps": 2,
        "De temps en temps": 1,
        "Jamais": 0
    }
    
    choix_psy = st.radio(
        label="Choisissez une option :",
        options=list(options_bien_etre.keys()),
        horizontal=True
    )
    score_psy = options_bien_etre[choix_psy]

    st.divider()

    # --- 3. FATIGUE ---
    st.write("### 3. Niveau de Fatigue (FACIT-F)")
    fatigue = st.slider("Intensité de votre fatigue :", 0, 10, 5)
    # Affichage du chiffre avec sa couleur
    st.markdown(f"**Intensité sélectionnée : {fatigue}** {get_status_circle(fatigue)}", unsafe_allow_html=True)

    st.write("")
    submitted = st.form_submit_button("Enregistrer les résultats dans le Cloud")

# --- ENREGISTREMENT ---
if submitted:
    new_entry = {
        "Date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Douleur": douleur,
        "Bien_etre_Score": score_psy,
        "Bien_etre_Texte": choix_psy,
        "Fatigue": fatigue
    }
    
    if conn:
        try:
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, pd.DataFrame([new_entry])], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ Données transmises au cloud.")
        except:
            st.error("❌ Erreur de connexion au Cloud.")
    else:
        st.info("📊 Mode local : Voici vos données (Connectez Google Sheets pour l'envoi cloud).")
        st.json(new_entry)
