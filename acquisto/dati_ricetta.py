from acquisto.carrello import *
from db import connection
import pandas as pd
from accesso.accesso import codice_utente
from acquisto.carrello import quanto_compro, carrello

def inserimento_dati_ricetta() -> int :
    count: int = 0
    i: int =0
    for prodotto in carrello:

        codice_val = prodotto["codice_farmaco"]
        query = f" SELECT ricetta FROM FarmaciMagazzino WHERE codice = '{codice_val}' AND ricetta = 'si'"
        serve_ricetta = pd.read_sql_query(query, connection)  # può restituire si o rimanere vuoto

        if not serve_ricetta.empty:
            codice_fiscale_utente = codice_utente()

            # controllo se l'utente è in possesso della ricetta per acquistare il farmaco
            query = f" SELECT codice_farmaco FROM Ricette WHERE codice_farmaco ='{codice_val}' AND codice_fiscale = '{codice_fiscale_utente}'"
            nome_ck = pd.read_sql_query(query, connection)
            if nome_ck.empty:
                print("Non è associata nessuna ricetta per questo farmaco al profilo corrente, il prodotto con ricetta verrà eliminato dal carrello")
                carrello.remove(prodotto)
                del quanto_compro [i]
            if not nome_ck.empty:
                count += 1
        i+=1
    return count