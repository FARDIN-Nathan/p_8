import streamlit as st
import requests
import numpy as np
import shap
import matplotlib.pyplot as plt

#Création de la page de features importances
st.set_page_config(page_title="Importance de vos données",page_icon="pad_banner.png")
st.title("Importance de vos données")
plt.style.use("seaborn-v0_8-colorblind")
# URL des APIs
url_gi = "https://6equal.pythonanywhere.com/importance-globale"
url_locale = "https://6equal.pythonanywhere.com/importance-locale"
plt.rcParams.update({'font.size': 14})
# Chargement des valeurs globales
if st.button("Charger les valeurs Globales"):
    response = requests.get(url_gi)

    if response.status_code == 200:
        data = response.json()
        feature_names = np.array(data["columns"])
        shap_values = np.array(data["shap_values"])

        if shap_values.shape[0] == len(feature_names):
            explainer = shap.Explanation(
                values=shap_values,
                base_values=0,
                feature_names=feature_names
            )

            st.write("Importance Globale des variables")
            fig, ax = plt.subplots()
            shap.plots.bar(explainer, show=False)
            st.pyplot(fig)
            st.caption("Graphique présentant les variables les plus influentes dans le choix du modèle")
        else:
            st.error("Erreur dans les dimensions des SHAP values.")
    else:
        st.error("Erreur lors de la récupération des données depuis l'API.")

# Choix de l'id client
st.write("Importance de vos variables spécifiques")
client_id = st.number_input("Veuillez renseigner l'ID client", min_value=0, max_value=999999, value=210611)

# Chargement des valeurs SHAP
if st.button("Charger les valeurs du client") and client_id:
    response = requests.get(f"{url_locale}/{client_id}")

    if response.status_code == 200:
        data = response.json()

        feature_names = np.array(data["columns"])
        shap_values = np.array(data["shap_values"])
        client_features = np.array(data["client_features"])
        base_value = data["base_value"]

        if shap_values.shape[0] == len(feature_names):
            explainer = shap.Explanation(
                values=shap_values,
                base_values=base_value,
                data=client_features,
                feature_names=feature_names
            )

            st.write(f"Importance des Features pour le client {client_id}")
            fig, ax = plt.subplots()
            shap.plots.waterfall(explainer, show=False)
            st.pyplot(fig)
            st.caption("Graphique présentant les variables les plus influentes pour votre prédiction")
        else:
            st.error("Erreur dans les dimensions.")
    else:
        st.error("Erreur lors de la récupération des données locales.")
