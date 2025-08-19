from db import connection
import pandas as pd




class Ricetta :
    id_utente :str

    def __init__(self, id_u):
        self.id_utente = id_u

    def verifica_dati_ricetta(self, carrello : list[dict], quantity: dict) -> int:

        count: int = 0
        nome_farma : str
        verifica_cod : bool = False
        ck: bool = False

        for prodotto in carrello:
            #si ricerca tra i prodotti nel carrello quelli che necessitano di ricetta
            codice_val = prodotto["codice_farmaco"]
            nome_farma = prodotto["nome"]
            query = f" SELECT ricetta FROM FarmaciMagazzino WHERE codice = '{codice_val}' AND ricetta = 'si'"
            serve_ricetta = pd.read_sql_query(query, connection)  # può restituire si o rimanere vuoto

            if not serve_ricetta.empty:

                # controllo se l'utente è in possesso della ricetta per acquistare il farmaco
                query = f" SELECT codice_ricetta, codice_farmaco , nome_medico FROM Ricetta WHERE codice_farmaco ='{codice_val}' AND codice_fiscale = '{self.id_utente}'"
                ricetta_ck = pd.read_sql_query(query, connection)

                if ricetta_ck.empty:

                    print(f"Non è associata nessuna ricetta per {nome_farma} al profilo corrente, il prodotto con ricetta verrà eliminato dal carrello")
                    carrello.remove(prodotto)
                    del quantity[prodotto["codice_farmaco"]]

                if not ricetta_ck.empty:

                    if len(ricetta_ck) > 1:
                        #se sono state prescritte più ricette si stampa quelle associate e si fa scegliere all'utente quale usare
                        for ricetta in ricetta_ck.to_dict(orient="records"):
                            print(ricetta)

                        while not ck:
                            codice_input = input("\nInserire il codice della ricetta che si vuole utilizzare : ")

                            for ricetta in ricetta_ck.to_dict(orient="records"):
                                if codice_input == ricetta["codice_ricetta"]:
                                    verifica_cod = True
                                    break

                            if not verifica_cod:
                                print("Il codice inserito non è valido, o non è presente tra quelli elencati")
                                ck = False
                            else:
                                ck = True

                    count += 1

        return count