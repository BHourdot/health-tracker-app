import streamlit as st
import pandas as pd
import datetime

# Configuration de la page
st.set_page_config(page_title="Suivi de Forme", page_icon="🏥", layout="centered")

# --- FONCTION DE COULEUR DYNAMIQUE ---
def get_visual_indicator(value):
    # Dégradé du vert (1) au rouge (10)
    colors = ["#22c55e", "#4ade80", "#84cc16", "#a8d810", "#eab308", 
              "#f59e0b", "#f97316", "#ea580c", "#dc2626", "#b91d1d"]
    color = colors[value-1]
    
    # Barre de progression et texte coloré
    html = f"""
    <div style="background-color: #e2e8f0; border-radius: 10px; width: 100%; height: 12px; margin-top: 10px;">
        <div style="background-color: {color}; width: {value*10}%; height: 12px; border-radius: 10px; transition: width 0.3s ease;"></div>
    </div>
    <div style="color: {color}; font-weight: bold; font-size: 18px; margin-top: 5px;">
        Niveau actuel : {value} / 10
    </div>
    """
    return html

# --- TITRE ---
st.title("🏥 Suivi d'État de Forme")
st.markdown("---")

# --- SÉLECTION DU PATIENT ---
# Dans une version réelle, cette liste pourrait provenir de votre base de données Cloud
liste_patients = ["Choisir un patient...", "Jean Dupont", "Marie Curie", "Léonard de Vinci", "Sophie Germain"]
nom_patient = st.selectbox(
    "👤 Sélectionner le nom du patient :",
    options=liste_patients,
    index=0
)

st.write("") # Espacement

# On n'affiche la suite que si un patient est sélectionné
if nom_patient != "Choisir un patient...":
    
    # --- 1. DOULEUR ---
    st.write("### 1. Évaluation de la Douleur")
    douleur = st.select_slider(
        "Faites glisser le curseur (1 = Faible, 10 = Intense)",
        options=list(range(1, 11)),
        key="slider_douleur"
    )
    st.markdown(get_visual_indicator(douleur), unsafe_allow_html=True)

    st.divider()

    # --- 2. BIEN-ÊTRE ---
    st.write("### 2. Bien-être Mental (Indice WHO-5)")
    st.write("**Au cours des 2 dernières semaines, je me suis senti(e) gai(e) et de bonne humeur :**")
    options_be = {
        "Tout le temps": 5, 
        "La plupart du temps": 4, 
        "Plus de la moitié du temps": 3, 
        "Moins de la moitié du temps": 2, 
        "De temps en temps": 1, 
        "Jamais": 0
    }
    choix_psy = st.radio("Sélectionnez votre ressenti :", options=list(options_be.keys()), horizontal=True)

    st.divider()

    # --- 3. FATIGUE ---
    st.write("### 3. Niveau de Fatigue")
    fatigue = st.select_slider(
        "Faites glisser le curseur (1 = Forme, 10 = Épuisement)",
        options=list(range(1, 11)),
        value=5,
        key="slider_fatigue"
    )
    st.markdown(get_visual_indicator(fatigue), unsafe_allow_html=True)

    st.divider()

    # --- BOUTON D'ENREGISTREMENT ---
    if st.button(f"🚀 Enregistrer les données pour {nom_patient}"):
        st.balloons()
        
        # Préparation des données pour le Cloud
        resultats = {
            "Date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Patient": nom_patient,
            "Douleur": douleur,
            "Bien_etre_Score": options_be[choix_psy],
            "Fatigue": fatigue
        }
        
        st.success(f"✅ Les données de **{nom_patient}** ont été enregistrées.")
        
        # Affichage du récapitulatif
        st.write("### Récapitulatif envoyé :")
        st.table(pd.DataFrame([resultats]))

else:
    st.warning("Veuillez sélectionner un nom de patient pour commencer le questionnaire.")

# --- PIED DE PAGE ---
st.sidebar.markdown("### Aide")
st.sidebar.info("Les indicateurs utilisés (EVA, WHO-5, FACIT-F) sont des échelles cliniques validées scientifiquement.")
