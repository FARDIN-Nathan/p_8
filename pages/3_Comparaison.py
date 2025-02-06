import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Comparaison entre le client et l'ensemble des données
st.title("Analyse entre vous et nos clients")

API_URL = "https://6equal.pythonanywhere.com/client"
POPULATION_URL = "https://6equal.pythonanywhere.com/population-data"

if "df_population" not in st.session_state:
    response_pop = requests.get(POPULATION_URL)
    if response_pop.status_code == 200:
        st.session_state.df_population = pd.DataFrame(response_pop.json())
    else:
        st.error("Erreur lors de la récupération des données de la population.")

df_population = st.session_state.df_population

client_id = st.text_input("Entrez l'ID du client", "")

if client_id and st.button("Récupérer les données du client"):
    response = requests.get(API_URL, params={"client_id": client_id})

    if response.status_code == 200:
        client_data = response.json()["data"]
        df_client = pd.DataFrame([client_data])

        st.subheader(f"Données du client {client_id}")
        st.dataframe(df_client)

        available_features = df_population.columns.tolist()
        feature_name = st.selectbox("Choisissez une variable", available_features)

        fig, ax = plt.subplots()
        sns.histplot(st.session_state.df_population[feature_name], color='grey', kde=True)
        ax.axvline(df_client[feature_name].values[0], color="blue", linestyle='--', linewidth=2)
        st.pyplot(fig)
    else:
        st.error("Erreur lors de la récupération des données du client.")
