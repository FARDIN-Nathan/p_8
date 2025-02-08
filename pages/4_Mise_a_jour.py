import streamlit as st
import requests
import pandas as pd

#Page pour la mise à jour des données et la nouvelle prédiction
st.title("Mise à jour de vos données et nouvelle prédiction")

API_URL = "https://6equal.pythonanywhere.com/client"

client_id = st.text_input("Entrez l'ID du client actuel", "")

if client_id and st.button("Récupérer les données"):
    response = requests.get(API_URL, params={"client_id": client_id})

    if response.status_code == 200:
        client_data = response.json()
        df_client = pd.DataFrame([client_data["data"]])

        st.subheader(f"Vos données, client numéro : {client_id}")
        st.dataframe(df_client)

        st.session_state.updated_data = client_data["data"]

if "updated_data" in st.session_state and st.session_state.updated_data:
    st.subheader("Modifier les valeurs")
    with st.container(height = 300):
        for feature, value in st.session_state.updated_data.items():
            if isinstance(value, (int)):
                st.session_state.updated_data[feature] = st.number_input(f"{feature}", value=int(value))

if st.button("Mettre à jour et prédire"):
    update_payload = {
        "client_id": int(client_id),
        "data": st.session_state.updated_data
    }

    update_response = requests.post(API_URL, json=update_payload)

    if update_response.status_code == 200:
        st.success("Mise à jour réussie et nouvelle prédiction obtenue !")
        prediction = update_response["prediction"]
        st.write(f"Prédiction : {prediction}")
    else:
        st.error("Erreur lors de la mise à jour.")
