import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Suivi État de Forme", page_icon="🏥", layout="centered")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2563eb; color: white; }
    .stProgress > div > div > div > div { background-color: #2563eb; }
    </style>
    """, unsafe_allow_html=True)

# --- TITRE ET INTRODUCTION ---
st.title("🏥 Mon Suivi de Santé")
st.subheader("Collecte d'indicateurs cliniques")
st.info("Ces questionnaires sont basés sur des échelles validées scientifiquement (EVA, WHO-5, FACIT-F).")

# --- FORMULAIRE DE COLLECTE ---
with st.form("health_form"):
    st.write("### 1. Évaluation de la Douleur (Échelle EVA)")
    douleur = st.select_slider(
        "Sur une échelle de 0 à 10, quel est votre niveau de douleur aujourd'hui ?",
        options=list(range(11)),
        help="0 = Aucune douleur, 10 = Douleur maximale imaginable"
    )

    st.divider()

    st.write("### 2. Bien-être Mental (Indice WHO-5)")
    st.caption("Au cours des deux dernières semaines...")
    psy_score = st.radio(
        "Je me suis senti(e) gai(e) et de bonne humeur :",
        ["Tout le temps (5)", "La plupart du temps (4)", "Plus de la moitié du temps (3)", 
         "Moins de la moitié du temps (2)", "De temps en temps (1)", "Jamais (0)"],
        horizontal=True
    )

    st.divider()

    st.write("### 3. Niveau de Fatigue (FACIT-F)")
    fatigue = st.slider("À quel point vous sentez-vous fatigué(e) ?", 0, 10, 5)

    # Bouton de soumission
    submitted = st.form_submit_button("Enregistrer les données")

# --- GESTION DES DONNÉES ---
if submitted:
    # Simulation de stockage (Dans une vraie app, on utiliserait une DB ou un CSV)
    data = {
        "Date": [datetime.date.today()],
        "Douleur": [douleur],
        "Bien-être": [int(psy_score[-2])],
        "Fatigue": [fatigue]
    }
    df = pd.DataFrame(data)
    
    st.success("✅ Données enregistrées avec succès !")
    
    # --- VISUALISATION ---
    st.write("### 📈 Aperçu de votre évolution")
    
    # Simulation d'historique pour le graphique
    history_data = {
        "Date": pd.date_range(end=datetime.date.today(), periods=5),
        "Score": [4, 6, 5, 7, (10 - fatigue)] # On inverse la fatigue pour le graphique
    }
    df_hist = pd.DataFrame(history_data)
    
    fig = px.line(df_hist, x="Date", y="Score", title="Évolution de la Vitalité (Score inverse de fatigue)",
                  markers=True, line_shape="spline")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# --- PIED DE PAGE ---
st.sidebar.title("Paramètres")
st.sidebar.write("Identifiant Patient: **#4092**")
if st.sidebar.button("Exporter les données (CSV)"):
    st.sidebar.write("Préparation du fichier...")
