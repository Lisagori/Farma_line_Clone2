from enum import unique
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Farmaline')

Base = declarative_base()

class SchedaTecnicaDB(Base) :
    __tablename__ = 'Schede_tecniche'

    codice= Column(Integer, primary_key= True, unique = True)
    indicazioni_terapeutiche = Column(String)
    composizione = Column(String)
    eccipienti =Column(String)
    controindicazioni = Column(String)
    posologia= Column(String)
    avvertenze = Column(String)
    effetti_indesiderati = Column(String)

Base.metadata.create_all(engine)