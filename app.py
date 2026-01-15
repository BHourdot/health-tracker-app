import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Configuration de la page
st.set_page_config(page_title="Saisie Indicateurs Santé", page_icon="📝")

# --- CONNEXION GOOGLE SHEETS ---
# Utilise les secrets configurés dans Streamlit Cloud ou .streamlit/secrets.toml
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erreur : Connexion au Google Sheet impossible. Vérifiez vos secrets.")
    conn = None

# --- FONCTION INDICATEUR VISUEL (COULEUR) ---
def get_visual_indicator(value):
    colors = ["#22c55e", "#4ade80", "#84cc16", "#a8d810", "#eab308", "#f59e0b", "#f97316", "#ea580c", "#dc2626", "#b91d1d"]
    color = colors[value-1]
    return f"""
    <div style="background-color: #e2e8f0; border-radius: 10px; width: 100%; height: 10px; margin-top: 10px;">
        <div style="background-color: {color}; width: {value*10}%; height: 10px; border-radius: 10px;"></div>
    </div>
    <div style="color: {color}; font-weight: bold; margin-top: 5px;">Score : {value}/10</div>
    """

st.title("🏥 Recueil des Données Patient")
st.markdown("Complétez les indicateurs ci-dessous pour les envoyer vers la base de données Drive.")

# --- SÉLECTION DU PATIENT ---
liste_patients = ["Choisir un patient...", "Jean Dupont", "Marie Curie", "Léonard de Vinci", "Sophie Germain"]
nom_patient = st.selectbox("👤 Nom du Patient :", options=liste_patients)

st.divider()

if nom_patient != "Choisir un patient...":
    # 1. DOULEUR
    st.write("### 1. Évaluation de la Douleur")
    douleur = st.select_slider("Intensité (1=Faible, 10=Max) :", options=list(range(1, 11)), key="d_slider")
    st.markdown(get_visual_indicator(douleur), unsafe_allow_html=True)
    
    st.write("")

    # 2. BIEN-ÊTRE
    st.write("### 2. Bien-être Mental")
    options_be = {"Tout le temps": 5, "La plupart du temps": 4, "Plus de la moitié du temps": 3, "Moins de la moitié du temps": 2, "De temps en temps": 1, "Jamais": 0}
    choix_be = st.radio("Senti(e) gai(e) et de bonne humeur :", list(options_be.keys()), horizontal=True)

    st.write("")

    # 3. FATIGUE
    st.write("### 3. Niveau de Fatigue")
    fatigue = st.select_slider("Intensité (1=Forme, 10=Épuisement) :", options=list(range(1, 11)), value=5, key="f_slider")
    st.markdown(get_visual_indicator(fatigue), unsafe_allow_html=True)

    st.divider()

    # --- BOUTON D'ENVOI ---
    if st.button(f"🚀 Envoyer les résultats de {nom_patient} vers Google Sheets"):
        if conn:
            # Préparation de la nouvelle ligne
            new_data = pd.DataFrame([{
                "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Patient": nom_patient,
                "Douleur": douleur,
                "Bien_etre": options_be[choix_be],
                "Fatigue": fatigue
            }])

            try:
                # Lecture des données existantes
                existing_data = conn.read()
                # Fusion et mise à jour
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(data=updated_df)
                
                st.balloons()
                st.success(f"✅ Données enregistrées dans le Google Sheet pour {nom_patient} !")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'envoi : {e}")
        else:
            st.warning("La connexion au Cloud n'est pas configurée.")
else:
    st.info("Veuillez sélectionner un patient pour activer le formulaire.")
