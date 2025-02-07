import streamlit as st
#Configuration du fichier de gestion
st.set_page_config(page_title="Prêt à dépenser", layout="wide")

st.title("Application de Prédiction de Capacité de Paiement")
st.write("Utilisez le menu latéral pour naviguer entre les différentes pages de l'application.")
st.image("pad_banner.png", caption="Logo de l'entreprise")
st.title("Explication des différentes pages")
st.write("Page 1: permet d'obtenir les prédictions d'accord de prêt pour un identifiant client défini")
st.write("Page 2:permet d'identifier les données ayant été les plus importantes pour la prédiction")
st.write("Page 3: permet de comparer les données du client avec celles des autres personnes présentes dans la base de données")
st.write("Page 4: permet de modifier des données client puis de demander une nouvelle prédiction")