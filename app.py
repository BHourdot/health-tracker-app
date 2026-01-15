import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Configuration de la page
st.set_page_config(page_title="Collecte Santé", page_icon="🏥", layout="centered")

# --- CONNEXION GOOGLE SHEETS ---
# L'URL est récupérée depuis les Secrets (voir étape suivante)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erreur de configuration Cloud. Vérifiez vos Secrets.")
    conn = None

# --- FONCTION INDICATEUR VISUEL ---
def get_visual_indicator(value):
    # Palette du vert (1) au rouge (10)
    colors = ["#22c55e", "#4ade80", "#84cc16", "#a8d810", "#eab308", 
              "#f59e0b", "#f97316", "#ea580c", "#dc2626", "#b91d1d"]
    color = colors[value-1]
    
    html = f"""
    <div style="background-color: #e2e8f0; border-radius: 10px; width: 100%; height: 10px; margin-top: 10px;">
        <div style="background-color: {color}; width: {value*10}%; height: 10px; border-radius: 10px; transition: width 0.3s ease;"></div>
    </div>
    <div style="color: {color}; font-weight: bold; font-size: 16px; margin-top: 5px;">
        Niveau : {value} / 10
    </div>
    """
    return html

# --- INTERFACE ---
st.title("🏥 Collecte d'Indicateurs Cliniques")
st.markdown("Veuillez renseigner les informations pour mettre à jour le dossier patient.")

# 0. SÉLECTION PATIENT
liste_patients = ["Choisir...", "Jean Dupont", "Marie Curie", "Isaac Newton", "Sophie Germain"]
nom_patient = st.selectbox("👤 Sélectionner le patient :", options=liste_patients)

st.divider()

if nom_patient != "Choisir...":
    # 1. DOULEUR (EVA)
    st.write("### 1. Évaluation de la Douleur (EVA)")
    douleur = st.select_slider(
        "1 = Douleur très faible | 10 = Douleur insupportable",
        options=list(range(1, 11)),
        key="s_douleur"
    )
    st.markdown(get_visual_indicator(douleur), unsafe_allow_html=True)

    st.divider()

    # 2. BIEN-ÊTRE (WHO-5)
    st.write("### 2. Bien-être Mental")
    st.write("**Au cours des 2 dernières semaines, je me suis senti(e) gai(e) et de bonne humeur :**")
    options_be = {
        "Tout le temps": 5, 
        "La plupart du temps": 4, 
        "Plus de la moitié du temps": 3, 
        "Moins de la moitié du temps": 2, 
        "De temps en temps": 1, 
        "Jamais": 0
    }
    choix_be = st.radio("Cochez votre ressenti :", options=list(options_be.keys()), horizontal=True)

    st.divider()

    # 3. FATIGUE (FACIT-F)
    st.write("### 3. Niveau de Fatigue")
    fatigue = st.select_slider(
        "1 = Forme olympique | 10 = Épuisement total",
        options=list(range(1, 11)),
        value=5,
        key="s_fatigue"
    )
    st.markdown(get_visual_indicator(fatigue), unsafe_allow_html=True)

    st.divider()

    # BOUTON D'ENREGISTREMENT
    if st.button(f"🚀 Enregistrer les données de {nom_patient}"):
        if conn:
            try:
                # Préparation des données
                new_row = pd.DataFrame([{
                    "Date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Patient": nom_patient,
                    "Douleur": douleur,
                    "Bien_etre": options_be[choix_be],
                    "Fatigue": fatigue
                }])

                # Lecture et mise à jour du Google Sheet
                existing_data = conn.read()
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(data=updated_df)

                st.balloons()
                st.success(f"Données enregistrées avec succès dans le cloud pour {nom_patient}.")
            except Exception as e:
                st.error(f"Erreur lors de l'envoi : {e}")
        else:
            st.error("Connexion Google Sheets non configurée.")

else:
    st.info("Veuillez sélectionner un patient pour commencer la saisie.")
