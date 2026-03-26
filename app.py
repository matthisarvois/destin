import streamlit as st
import pandas as pd
from crud import (
    ajouter_utilisateur,
    ajouter_donnee,
    get_donnees_utilisateur,
    get_utilisateur_par_email
)
from database import init_db

init_db()

st.title("Mon Application Multi-Utilisateur")

# --- Connexion simple par email ---
email = st.text_input("Votre email pour vous identifier")

if email:
    user = get_utilisateur_par_email(email)

    if user is None:
        st.info("Première visite ! Créons votre compte.")
        nom = st.text_input("Votre nom")
        if st.button("Créer mon compte") and nom:
            user = ajouter_utilisateur(nom, email)
            st.success(f"Bienvenue {nom} !")
            st.rerun()
    else:
        st.success(f"Connecté en tant que {user.nom}")

        # --- Ajouter des données ---
        st.subheader("Ajouter une donnée")
        col1, col2 = st.columns(2)
        valeur = col1.number_input("Valeur", step=0.1)
        categorie = col2.selectbox("Catégorie", ["Vente", "Achat", "Autre"])

        if st.button("Ajouter"):
            ajouter_donnee(user.id, valeur, categorie)
            st.success("Donnée ajoutée !")
            st.rerun()

        # --- Voir ses données (uniquement les siennes) ---
        st.subheader("Vos données")
        donnees = get_donnees_utilisateur(user.id)

        if donnees:
            df = pd.DataFrame([
                {
                    "Valeur": d.valeur,
                    "Catégorie": d.categorie,
                    "Date": d.date_ajout
                }
                for d in donnees
            ])
            st.dataframe(df)
            st.metric("Total", f"{df['Valeur'].sum():.2f}")
        else:
            st.info("Aucune donnée pour l'instant")