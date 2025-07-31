from enum import unique
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Farmaline')

Base = declarative_base()

class RicettaMedicaDB(Base) :
    __tablename__ = 'ricette_mediche'


class PrescrizioneMedicaDB(Base) :
    __tablename__ = 'prescrizioni_mediche'

Base.metadata.create_all(engine)