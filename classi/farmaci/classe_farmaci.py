
class Farmaco:
    codice: str
    nome: str
    ricetta: str
    preparato_galenico: str
    prezzo: str

    def __init__(self, codice: str, nome: str, prezzo: str, ricetta: str, preparato_galenico: str, scheda_tecnica=None):
        self.codice = codice
        self.nome = nome
        self.prezzo = prezzo
        self.ricetta = ricetta
        self.preparato_galenico = preparato_galenico
        self.scheda_tecnica = scheda_tecnica  # opzionale
