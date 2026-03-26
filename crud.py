from database import (
    SessionLocal,
    Utilisateur,
    Donnee
)

def ajouter_utilisateur(
        nom : str,
        email : str,
        age : int,
        sexe : str | None=None
) -> Utilisateur:
    session = SessionLocal()
    try :
        user = Utilisateur(nom = nom,email= email, age= age,sexe=sexe)
        session.add(user) #la on ajoute l'utilisateur dans la session
        session.commit() #la on sauvegarde
        session.refresh(user) #On récupère l'id généré
        return user
    finally:
        session.close()


def ajouter_donnee(
        utilisateur_id  : int,
        valeur : float,
        categorie : str | None = None
)->Donnee:
    session = SessionLocal()
    try:
        donnee = Donnee(
            utilisateur_id = utilisateur_id,
            valeur = valeur,
            categorie = categorie
        )
        session.add(donnee)
        session.commit()
        return donnee
    finally:
        session.close()


def ajouter_donnees_en_lot(
        utilisateur_id, 
        liste_donnees):
    """Ajoute PLUSIEURS lignes d'un coup, toujours sans toucher l'existant."""
    session = SessionLocal()
    try:
        nouvelles = [
            Donnee(
                utilisateur_id=utilisateur_id,
                valeur=d["valeur"],
                categorie=d["categorie"]
            )
            for d in liste_donnees
        ]
        session.add_all(nouvelles)  # INSERT multiple
        session.commit()
        return len(nouvelles)
    finally:
        session.close()

   

def get_donnees_utilisateur(utilisateur_id):
    """Récupère toutes les données d'UN utilisateur (pas celles des autres)."""
    session = SessionLocal()
    try:
        return session.query(Donnee).filter(
            Donnee.utilisateur_id == utilisateur_id
        ).all()
    finally:
        session.close()


def get_utilisateur_par_email(email):
    session = SessionLocal()
    try:
        return session.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()
    finally:
        session.close()