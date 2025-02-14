import streamlit as st
import requests
import pandas as pd

#Page pour la mise à jour des données clients
st.set_page_config(page_title="Mise à jour de vos données et nouvelle prédiction",page_icon="pad_banner.png")
st.title("Mise à jour de vos données et nouvelle prédiction")

API_URL = "https://6equal.pythonanywhere.com/client"
FEATURES_URL = "https://6equal.pythonanywhere.com/features"

client_id = st.number_input("Entrez l'ID du client pour l'ajouter ou pour modifier ses données", min_value=0, max_value=999999, value=210611)
#Récuperation des données clients
if client_id and st.button("Récupérer les données"):
    r = requests.get(API_URL, params={"client_id": client_id})
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame([data["data"]])
        st.session_state.df_client = df
    elif r.status_code == 404:
        feat = requests.get(FEATURES_URL)
        if feat.status_code == 200:
            features = feat.json().get("features", [])
            df = pd.DataFrame([[0]*len(features)], columns=features)
            df["SK_ID_CURR"] = int(client_id)
            st.session_state.df_client = df
        else:
            st.error("Impossible de récupérer la liste des features.")
    else:
        st.error(f"Erreur : {r.status_code}")
        st.error(r.text)
#Sauvegarde des données
if "df_client" in st.session_state:
    edited_df = st.data_editor(st.session_state.df_client, num_rows="fixed")
    st.session_state.df_client = edited_df
#Nouvelle prediction à partir des données maj
if st.button("Mettre à jour et prédire"):
    if "df_client" in st.session_state:
        df = st.session_state.df_client.copy()
        df.fillna(0, inplace=True)
        for c in df.columns:
            df[c] = df[c].astype(int, errors="ignore")
        data_dict = df.iloc[0].to_dict()
        payload = {"client_id": int(client_id), "data": data_dict}
        res = requests.post(API_URL, json=payload)
        if res.status_code == 200:
            response = res.json()
            prediction = response["prediction"]
            details = response["details"]
            st.success("Mise à jour ou création effectuée.")
            st.write(f"Prédiction : {prediction} le statut du crédit est donc {details}*")
            st.write("grant_loan : crédit accordé")
            st.write("do_not_grant_loan : crédit refusé")
            
        else:
            st.error(f"Erreur : {res.status_code}")
            st.error(res.text)
