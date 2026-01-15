import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Configuration de la page
st.set_page_config(page_title="Santé Connectée", page_icon="🏥")

# --- FONCTION POUR LA COULEUR ---
def get_color(value):
    # Du vert (0) au rouge (10)
    colors = ["#22c55e", "#4ade80", "#84cc16", "#a8d810", "#eab308", 
              "#f59e0b", "#f97316", "#ea580c", "#dc2626", "#b91d1d", "#7f1d1d"]
    return colors[int(value)]

# --- CONNEXION CLOUD (Google Sheets) ---
# Note : Nécessite la configuration des secrets sur Streamlit Cloud
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    conn = None

# --- STYLE CSS ---
st.markdown(f"""
    <style>
    .stSlider [data-baseweb="slider"] {{ background-image: linear-gradient(to right, #22c55e, #eab308, #dc2626); border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 Suivi d'État de Forme")

with st.form("health_form"):
    # --- DOULEUR ---
    st.write("### 1. Niveau de Douleur (EVA)")
    douleur = st.select_slider("Glissez pour évaluer", options=list(range(11)), value=0)
    st.markdown(f'<div style="height:10px; width:100%; background-color:{get_color(douleur)}; border-radius:5px;"></div>', unsafe_allow_html=True)
    
    st.divider()

    # --- BIEN-ÊTRE ---
    st.write("### 2. Bien-être Mental (WHO-5)")
    psy_score = st.radio("Sensation de gaieté :", [5, 4, 3, 2, 1, 0], horizontal=True, 
                         help="5 = Tout le temps, 0 = Jamais")

    st.divider()

    # --- FATIGUE ---
    st.write("### 3. Niveau de Fatigue (FACIT-F)")
    fatigue = st.slider("Intensité de la fatigue", 0, 10, 5)
    st.markdown(f'<div style="height:10px; width:100%; background-color:{get_color(fatigue)}; border-radius:5px;"></div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("Envoyer les résultats au Cloud")

# --- GESTION DU CLOUD ---
if submitted:
    new_data = pd.DataFrame([{
        "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Douleur": douleur,
        "Bien_etre": psy_score,
        "Fatigue": fatigue
    }])

    if conn:
        try:
            # Récupérer les données existantes et ajouter les nouvelles
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ Données synchronisées avec le Google Sheet !")
        except Exception as e:
            st.warning("⚠️ Connecté mais impossible d'écrire. Vérifiez les permissions.")
    else:
        st.info("💡 Mode démo : Les données seraient envoyées sur votre Cloud ici.")
        st.table(new_data)
