import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Comparaison entre le client et l'ensemble des données
st.set_page_config(page_title="Analyse entre vous et nos clients",page_icon="pad_banner.png")
st.title("Analyse entre vous et nos clients")
plt.rcParams.update({'font.size': 14})
API_URL = "https://6equal.pythonanywhere.com/client"
POPULATION_URL = "https://6equal.pythonanywhere.com/population-data"
sns.set_palette("colorblind")
AVAILABLE_FEATURES = [
    "CNT_CHILDREN", "OBS_30_CNT_SOCIAL_CIRCLE", "EXT_SOURCE_1",
    "EXT_SOURCE_2", "EXT_SOURCE_3", "COUNT_FAM_MEMBERS", "PAYMENT_RATE"
]

if "df_population" not in st.session_state:
    response_pop = requests.get(POPULATION_URL)
    if response_pop.status_code == 200:
        st.session_state.df_population = pd.DataFrame(response_pop.json())
    else:
        st.error("Erreur lors de la récupération des données de la population.")

df_population = st.session_state.df_population

if "client_data" not in st.session_state:
    st.session_state.client_data = None

client_id = st.number_input("Entrez l'ID du client", min_value=0, max_value=999999, value=210611)
# Récupération des valeurs clients
if client_id:
    if st.button("Récupérer les données du client") or st.session_state.client_data:
        if st.session_state.client_data is None:
            response = requests.get(API_URL, params={"client_id": client_id})
            if response.status_code == 200:
                st.session_state.client_data = response.json()["data"]
            else:
                st.error(f"Erreur : {response.json().get('error', 'Problème rencontré')}")

        if st.session_state.client_data:
            df_client = pd.DataFrame([st.session_state.client_data])

            if df_population.empty:
                st.error("Les données de population ne sont pas disponibles.")
            else:
                st.write(f"Données du client {client_id}")
                st.dataframe(df_client.style.format("{:.2f}"))

                feature_name = st.selectbox("Choisissez une variable", AVAILABLE_FEATURES)
                fig, ax = plt.subplots()
                sns.histplot(df_population[feature_name], kde=True)

                # Calcul de la moyenne de la population
                mean_value = df_population[feature_name].mean()

                # Ajout des lignes pour la moyenne et le client
                ax.axvline(float(df_client[feature_name].values[0]), linestyle="dotted", linewidth=2, label=f'Client {client_id}')
                ax.axvline(float(mean_value), color="black", linestyle="dashdot", linewidth=2, label='Moyenne de la population')

                ax.set(title=f'Comparaison avec la population pour {feature_name}', ylabel='')
                plt.grid(axis='y')
                plt.legend()
                st.pyplot(fig)
                st.caption("Graphique présentant vos données face à celles des autres clients")

                st.write("Analyse de corrélation entre deux variables")

                # Sélection des deux features à comparer
                feature_name_1 = st.selectbox("Variable 1", AVAILABLE_FEATURES, index=0)
                feature_name_2 = st.selectbox("Variable 2", AVAILABLE_FEATURES, index=1)

                if feature_name_1 in df_population.columns and feature_name_2 in df_population.columns:
                    df_correlation = df_population[[feature_name_1, feature_name_2]].dropna()

                    # Calcul de la matrice de corrélation
                    correlation_matrix = df_correlation.corr()

                    # Affichage de la heatmap
                    fig, ax = plt.subplots(figsize=(5, 4))
                    sns.heatmap(correlation_matrix, annot=True, cmap="cividis", center=0, fmt=".2f", linewidths=0.5, ax=ax)

                    ax.set_title(f"Corrélation entre {feature_name_1} et {feature_name_2}")

                    st.pyplot(fig)
                    st.caption("Graphique présentant les relations entre les deux variables sélectionné")
                else:
                    st.error("Les features sélectionnées ne sont pas disponibles dans les données.")
