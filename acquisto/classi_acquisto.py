
class Farmaco :

    codice : str
    nome : str
    ricetta : str
    preparato_galenico : str
    prezzo : str
# TODO trovare modo di associare dati da database a classe
    def __init__(self,codice : str, nome: str, prezzo: str, ricetta: str, preparato_galenico: str):
        self.codice = codice
        self.nome = nome
        self.prezzo = prezzo
        self.ricetta = ricetta
        self.preparato_galenico = preparato_galenico
