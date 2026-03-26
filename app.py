import streamlit as st
import os
import pandas as pd
from crud import (
    ajouter_utilisateur,
    ajouter_donnee,
    get_tous_utilisateurs,
    get_toutes_donnees
)

mdpasse = os.getenv("MDP")

st.set_page_config(page_title="Gestion Clients", layout="wide")
st.title("Gestion de Base de Données")

tab_saisie, tab_consultation = st.tabs(["Saisie", "Consultation"])


# ==================== SAISIE ====================
with tab_saisie:

    st.header("Nouvel utilisateur")
    with st.form("form_utilisateur", clear_on_submit=True):
        nom = st.text_input("Nom *")
        email = st.text_input("Email *")
        age = st.number_input("Âge *", min_value=1, max_value=150, step=1)
        sexe = st.selectbox("Sexe (optionnel)", ["Non renseigné", "Homme", "Femme", "Autre"])
        submit_user = st.form_submit_button("Ajouter l'utilisateur")

    if submit_user:
        if not nom or not email:
            st.error("Le nom et l'email sont obligatoires.")
        else:
            sexe_val = None if sexe == "Non renseigné" else sexe
            try:
                user = ajouter_utilisateur(nom, email, age, sexe_val)
                st.success(f"Utilisateur '{nom}' ajouté avec l'ID {user.id} !")
            except Exception as e:
                st.error(f"Erreur : {e}")

    st.divider()
    st.header("Nouvelle donnée")

    utilisateurs = get_tous_utilisateurs()

    if not utilisateurs:
        st.info("Aucun utilisateur enregistré. Ajoutez-en un d'abord.")
    else:
        options = {f"{u.nom} (ID: {u.id})": u.id for u in utilisateurs}

        with st.form("form_donnee", clear_on_submit=True):
            user_choisi = st.selectbox("Utilisateur", options.keys())
            valeur = st.number_input("Valeur", step=0.1)
            categorie = st.selectbox("Catégorie", ["Vente", "Achat", "Autre"])
            submit_donnee = st.form_submit_button("Ajouter la donnée")

        if submit_donnee:
            try:
                ajouter_donnee(options[user_choisi], valeur, categorie)
                st.success("Donnée ajoutée !")
            except Exception as e:
                st.error(f"Erreur : {e}")

# ==================== CONSULTATION ====================
with tab_consultation:

    if "acces_autorise" not in st.session_state:
        st.session_state.acces_autorise = False

    if not st.session_state.acces_autorise:
        mdp = st.text_input("Mot de passe pour accéder aux données", type="password")
        if st.button("Valider"):
            if mdp == mdpasse:
                st.session_state.acces_autorise = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")
    else:
        st.header("Utilisateurs")
        utilisateurs = get_tous_utilisateurs()

        if utilisateurs:
            df_users = pd.DataFrame([
                {
                    "ID": u.id,
                    "Nom": u.nom,
                    "Email": u.email,
                    "Âge": u.age,
                    "Sexe": u.sexe or "Non renseigné"
                }
                for u in utilisateurs
            ])
            st.dataframe(df_users, use_container_width=True)
            st.metric("Nombre d'utilisateurs", len(utilisateurs))
        else:
            st.info("Aucun utilisateur enregistré.")

        st.divider()
        st.header("Données")
        donnees = get_toutes_donnees()

        if donnees:
            df_donnees = pd.DataFrame([
                {
                    "ID": d.id,
                    "Utilisateur ID": d.utilisateur_id,
                    "Valeur": d.valeur,
                    "Catégorie": d.categorie,
                    "Date ajout": d.date_ajout
                }
                for d in donnees
            ])
            st.dataframe(df_donnees, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Nombre d'entrées", len(donnees))
            col2.metric("Total valeurs", f"{df_donnees['Valeur'].sum():.2f}")
            col3.metric("Moyenne", f"{df_donnees['Valeur'].mean():.2f}")
        else:
            st.info("Aucune donnée enregistrée.")

        st.divider()
        if st.button("Se déconnecter"):
            st.session_state.acces_autorise = False
            st.rerun()