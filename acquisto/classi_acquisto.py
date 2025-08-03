from ricerca.base_medicinali import FarmaciDB

class Farmaco:

    def __init__(self, codice: str, nome: str, prezzo: str, ricetta: str, preparato_galenico: str, scheda_tecnica=None):
        self.codice = codice
        self.nome = nome
        self.prezzo = prezzo
        self.ricetta = ricetta
        self.preparato_galenico = preparato_galenico
        self.scheda_tecnica = scheda_tecnica  # opzionale

    @classmethod
    def from_db(farmaco_db: FarmaciDB) -> "Farmaco": #associo gli attributi della classe alle colonne della tabella del databse
        return Farmaco(
            codice=farmaco_db.codice,
            nome=farmaco_db.nome,
            prezzo=farmaco_db.prezzo,
            ricetta=farmaco_db.ricetta,
            preparato_galenico=farmaco_db.preparato_galenico,
            scheda_tecnica=farmaco_db.scheda_tecnica  # se presente
        )
#non si puo fare tutto in init