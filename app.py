import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Configuration de la page
st.set_page_config(page_title="Santé Connectée", page_icon="🏥")

# --- FONCTION POUR LA COULEUR DYNAMIQUE (HEXADÉCIMAL) ---
def get_color(value):
    # Dégradé du vert (1) au rouge (10)
    colors = {
        1: "#22c55e", 2: "#4ade80", 3: "#84cc16", 4: "#a8d810", 
        5: "#eab308", 6: "#f59e0b", 7: "#f97316", 8: "#ea580c", 
        9: "#dc2626", 10: "#b91d1d"
    }
    return colors.get(value, "#2563eb")

# --- CONNEXION CLOUD ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    conn = None

st.title("🏥 Suivi d'État de Forme")

# --- FORMULAIRE ---
with st.form("health_form"):
    
    # --- 1. DOULEUR ---
    st.write("### 1. Évaluation de la Douleur (EVA)")
    douleur = st.select_slider(
        "Niveau de douleur (1 = très faible, 10 = insupportable) :",
        options=list(range(1, 11)),
        value=1
    )
    
    # Injection CSS pour colorer le bouton du slider Douleur
    st.markdown(f"""
        <style>
        div[data-testid="stTickBar"] + div div[role="slider"] {{
            background-color: {get_color(douleur)} !important;
            border: 2px solid white !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    st.divider()

    # --- 2. BIEN-ÊTRE ---
    st.write("### 2. Bien-être Mental (Indice WHO-5)")
    st.write("**Au cours des 2 dernières semaines, je me suis senti(e) gai(e) et de bonne humeur :**")
    
    options_bien_etre = {
        "Tout le temps": 5,
        "La plupart du temps": 4,
        "Plus de la moitié du temps": 3,
        "Moins de la moitié du temps": 2,
        "De temps en temps": 1,
        "Jamais": 0
    }
    
    choix_psy = st.radio("Sélectionnez votre ressenti :", options=list(options_bien_etre.keys()), horizontal=True)
    score_psy = options_bien_etre[choix_psy]

    st.divider()

    # --- 3. FATIGUE ---
    st.write("### 3. Niveau de Fatigue (FACIT-F)")
    # Note: Streamlit utilise le même sélecteur CSS pour tous les sliders de la page.
    # Pour colorer spécifiquement le 2ème slider différemment, nous utilisons la valeur actuelle.
    fatigue = st.slider("Intensité de votre fatigue (1 à 10) :", 1, 10, 5)
    
    st.markdown(f"**Score Fatigue :** {fatigue} / 10")

    st.write("")
    submitted = st.form_submit_button("Enregistrer les résultats dans le Cloud")

# --- ENREGISTREMENT ---
if submitted:
    new_entry = {
        "Date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Douleur": douleur,
        "Bien_etre_Score": score_psy,
        "Fatigue": fatigue
    }
    
    if conn:
        try:
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, pd.DataFrame([new_entry])], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ Données envoyées avec succès !")
        except:
            st.error("❌ Erreur de connexion au Cloud.")
    else:
        st.info("📊 Mode local : Données prêtes pour le Cloud.")
        st.table(pd.DataFrame([new_entry]))
