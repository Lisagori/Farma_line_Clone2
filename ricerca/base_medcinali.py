from enum import unique
from operator import index

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from ricerca.documentazione_farmaci.base_documenti_medicinali import SchedaTecnicaDB

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Farmaline')

Base = declarative_base()

class FarmaciDB(Base) :
    __tablename__ = 'farmaci_in_magazzino'

    codice = Column( Integer, ForeignKey(SchedaTecnicaDB.codice), primary_key= True, unique=True)
    nome = Column(String)
    ricetta = Column (String(2), nullable=True)
    preparato_galenico = Column(String(2), nullable=True)
    prezzo = Column( String )

    def __repr__(self): #metodo speciale per definire la rappresentazione testuale di un oggetto
        return f"""codice : {self.codice} 
NOME : {self.nome} 
RICETTA : {self.ricetta} 
PREPARATO GALENICO : {self.preparato_galenico} 
PREZZO : {self.prezzo} 
"""

Base.metadata.create_all(engine)