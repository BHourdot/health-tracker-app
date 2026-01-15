import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Dashboard Santé", layout="wide")

# --- CONNEXION CLOUD ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Chargement des données historiques
    df_history = conn.read()
except:
    st.error("Impossible de se connecter au Cloud. Vérifiez vos secrets.")
    df_history = pd.DataFrame()

# --- INTERFACE ---
st.title("🏥 Analyse de l'État de Forme")

# Création de deux onglets : un pour la saisie, un pour l'analyse
tab1, tab2 = st.tabs(["📝 Saisie Patient", "📈 Historique & Analyse"])

with tab1:
    st.info("Utilisez cet onglet pour enregistrer de nouvelles données (voir code précédent).")
    # Insérez ici votre code de saisie précédent...

with tab2:
    if not df_history.empty:
        st.subheader("Visualisation de l'évolution temporelle")
        
        # Filtre par patient
        patients = df_history["Patient"].unique()
        patient_sel = st.selectbox("Sélectionnez un patient pour voir son historique :", patients)
        
        # Filtrage des données
        df_patient = df_history[df_history["Patient"] == patient_sel].copy()
        df_patient["Date"] = pd.to_datetime(df_patient["Date"])
        df_patient = df_patient.sort_values("Date")

        # Affichage des graphiques sur deux colonnes
        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Évolution de la Douleur")
            fig_douleur = px.line(
                df_patient, x="Date", y="Douleur", 
                title=f"Douleur - {patient_sel}",
                markers=True, line_shape="spline",
                color_discrete_sequence=["#dc2626"] # Rouge
            )
            fig_douleur.update_yaxes(range=[0, 11])
            st.plotly_chart(fig_douleur, use_container_width=True)

        with col2:
            st.write("#### Évolution de la Fatigue")
            fig_fatigue = px.line(
                df_patient, x="Date", y="Fatigue", 
                title=f"Fatigue - {patient_sel}",
                markers=True, line_shape="spline",
                color_discrete_sequence=["#f59e0b"] # Orange
            )
            fig_fatigue.update_yaxes(range=[0, 11])
            st.plotly_chart(fig_fatigue, use_container_width=True)

        # Affichage du tableau brut
        with st.expander("Voir les données brutes"):
            st.dataframe(df_patient)
    else:
        st.warning("Aucune donnée trouvée dans le Cloud pour générer les graphiques.")
