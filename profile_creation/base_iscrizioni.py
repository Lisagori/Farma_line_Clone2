from enum import unique
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import declarative_base, foreign

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Farmaline')

Base = declarative_base()

class TesseraSanitariaDB(Base):
    __tablename__ = 'tessere_sanitarie'

    codice_fiscale = Column(String, primary_key=True)
    sesso = Column(String)
    luogo_nascita = Column(String)
    provincia = Column(String)
    data_nascita = Column(String)
    data_scadenza = Column(String)
    numero_identificazione_tessera = Column(String)

class ClienteDB(Base):
    __tablename__ = 'clienti'

    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    codice_fiscale = Column(String,ForeignKey("tessere_sanitarie.codice_fiscale"),primary_key=True, nullable=False)

class TesserinoProfessionaleDB(Base):
    __tablename__ = 'tesserino_professionale'

    n_matricola = Column(String, primary_key=True, unique=True)
    ordine_di_appartenenza = Column(String)

class FarmacistaDB(Base):
    __tablename__ = 'farmacisti'

    nome = Column(String(100), nullable=False)
    cognome = Column(String(100), nullable=False)
    matricola = Column(String, ForeignKey('tesserino_professionale.n_matricola'),primary_key=True, nullable=False, unique=True)

Base.metadata.create_all(engine)

