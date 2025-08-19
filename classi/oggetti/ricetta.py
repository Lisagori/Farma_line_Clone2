import pandas as pd

from db import connection


class Ricetta :
    id_utente :str

    def __init__(self, id_u):
        self.id_utente = id_u

    def verifica_dati_ricetta(self, carrello : list[dict], quantity) -> int:

        count: int = 0
        nome_farma : str

        for prodotto in carrello:
            #si ricerca tra i prodotti nel carrello quelli che necessitano di ricetta
            codice_val = prodotto["codice_farmaco"]
            nome_farma = prodotto["nome"]
            query = f" SELECT ricetta FROM FarmaciMagazzino WHERE codice = '{codice_val}' AND ricetta = 'si'"
            serve_ricetta = pd.read_sql_query(query, connection)  # può restituire si o rimanere vuoto

            if not serve_ricetta.empty:

                # controllo se l'utente è in possesso della ricetta per acquistare il farmaco
                query = f" SELECT codice_farmaco FROM Ricetta WHERE codice_farmaco ='{codice_val}' AND codice_fiscale = '{self.id_utente}'"
                nome_ck = pd.read_sql_query(query, connection)

                if nome_ck.empty:

                    print(f"Non è associata nessuna ricetta per {nome_farma} al profilo corrente, il prodotto con ricetta verrà eliminato dal carrello")
                    carrello.remove(prodotto)
                    del quantity[prodotto["codice_farmaco"]]

                if not nome_ck.empty:
                    count += 1

        return count