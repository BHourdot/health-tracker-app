import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURATION ---
st.set_page_config(page_title="Santé Connectée", layout="wide", page_icon="🏥")

# --- CONNEXION CLOUD ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erreur de connexion au Cloud.")
    conn = None

# --- FONCTIONS UTILITAIRES ---
def get_visual_indicator(value):
    colors = ["#22c55e", "#4ade80", "#84cc16", "#a8d810", "#eab308", "#f59e0b", "#f97316", "#ea580c", "#dc2626", "#b91d1d"]
    color = colors[value-1]
    return f"""
    <div style="background-color: #e2e8f0; border-radius: 10px; width: 100%; height: 10px; margin-top: 10px;">
        <div style="background-color: {color}; width: {value*10}%; height: 10px; border-radius: 10px;"></div>
    </div>
    <div style="color: {color}; font-weight: bold; margin-top: 5px;">Niveau : {value}/10</div>
    """

# --- MENU LATÉRAL ---
st.sidebar.title("🩺 Navigation")
page = st.sidebar.radio("Aller vers :", ["📝 Recueil des données", "📊 Visualisation Historique"])

# ==========================================
# PAGE 1 : RECUEIL DES DONNÉES
# ==========================================
if page == "📝 Recueil des données":
    st.title("📝 Saisie des indicateurs")
    
    liste_patients = ["Choisir...", "Jean Dupont", "Marie Curie", "Isaac Newton"]
    nom_patient = st.selectbox("👤 Patient :", options=liste_patients)

    if nom_patient != "Choisir...":
        with st.container():
            st.write("### 1. Douleur")
            douleur = st.select_slider("Intensité :", options=list(range(1, 11)), key="d1")
            st.markdown(get_visual_indicator(douleur), unsafe_allow_html=True)
            
            st.divider()
            
            st.write("### 2. Bien-être (WHO-5)")
            options_be = {"Tout le temps": 5, "Souvent": 4, "Parfois": 3, "Rarement": 2, "Jamais": 0}
            choix_be = st.radio("Senti(e) gai(e) et de bonne humeur :", list(options_be.keys()), horizontal=True)
            
            st.divider()
            
            st.write("### 3. Fatigue")
            fatigue = st.select_slider("Intensité :", options=list(range(1, 11)), value=5, key="f1")
            st.markdown(get_visual_indicator(fatigue), unsafe_allow_html=True)

            if st.button(f"Enregistrer pour {nom_patient}"):
                new_data = pd.DataFrame([{
                    "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "Patient": nom_patient,
                    "Douleur": douleur,
                    "Bien_etre": options_be[choix_be],
                    "Fatigue": fatigue
                }])
                if conn:
                    df_existing = conn.read()
                    updated_df = pd.concat([df_existing, new_data], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Données sauvegardées !")
    else:
        st.warning("Veuillez sélectionner un patient.")

# ==========================================
# PAGE 2 : VISUALISATION
# ==========================================
else:
    st.title("📊 Analyse de l'évolution")
    
    if conn:
        df = conn.read()
        if not df.empty:
            patient_sel = st.selectbox("Sélectionner un patient à analyser :", df["Patient"].unique())
            df_p = df[df["Patient"] == patient_sel].copy()
            df_p["Date"] = pd.to_datetime(df_p["Date"])
            df_p = df_p.sort_values("Date")

            # Graphique combiné
            st.write(f"### Courbes de suivi : {patient_sel}")
            
            # Transformation pour Plotly (format long)
            df_melted = df_p.melt(id_vars=['Date'], value_vars=['Douleur', 'Fatigue'], 
                                  var_name='Indicateur', value_name='Score')
            
            fig = px.line(df_melted, x="Date", y="Score", color="Indicateur",
                          markers=True, line_shape="spline",
                          color_discrete_map={"Douleur": "#dc2626", "Fatigue": "#f59e0b"})
            
            fig.update_layout(yaxis=dict(range=[0, 11]), hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

            # Statistiques rapides
            c1, c2, c3 = st.columns(3)
            c1.metric("Douleur Moyenne", round(df_p["Douleur"].mean(), 1))
            c2.metric("Fatigue Moyenne", round(df_p["Fatigue"].mean(), 1))
            c3.metric("Bien-être (Dernier)", df_p["Bien_etre"].iloc[-1])
        else:
            st.info("Aucune donnée disponible dans le Cloud.")
