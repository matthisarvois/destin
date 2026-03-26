import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship
)
from datetime import datetime

load_dotenv()

#connexion à la base distante avec le lien dans le fichier .env
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()


#On défini les tables avec  les classses


class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String,nullable=False)
    email = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    sexe = Column(String,nullable= True)

    #les relations entre les bases de données*
    donnees = relationship("Donnee",back_populates="utilisateur")


class Donnee(Base):
    __tablename__ = "donnees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    valeur = Column(Float, nullable=False)
    categorie = Column(String)
    date_ajout = Column(DateTime, default=datetime.now)  # <-- pour l'incrémental plus tard
    
    utilisateur =  relationship("Utilisateur",back_populates="donnees")


def init_db():
    Base.metadata.create_all(engine)


if __name__=="__main__":
    init_db()
    print("Tables crées avec succès !!!!")

