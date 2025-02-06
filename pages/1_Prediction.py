import streamlit as st
import requests
import plotly.graph_objects as go

#Création de la page de prédiction et d'affichage
st.title("Prédiction de capacité de paiement du client")

user_id = st.number_input("Veuillez renseigner l'ID du client", min_value=0, max_value=999999, value=210611)
url_api = f"https://6equal.pythonanywhere.com/predict/{user_id}"

if st.button("Obtenir la prédiction"):
    response = requests.get(url_api)
    
    if response.status_code == 200:
        response = response.json()
        prediction = response["prediction"]
        probability_pay = response["probability"]["will_pay"]

        st.write(f"Prédiction : {prediction}")
        
        #Affichage d'une jauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value= probability_pay * 100,
            title={"text": "Score de fiabilité crédit (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "blue"},
                "steps": [
                    {"range": [0, 25], "color": "red"},
                    {"range": [25, 50], "color": "orange"},
                    {"range": [50, 75], "color": "yellow"},
                    {"range": [75, 100], "color": "green"}
                ]
            }
        ))
        st.plotly_chart(fig)
    else:
        st.error("Erreur lors de la requête API.")