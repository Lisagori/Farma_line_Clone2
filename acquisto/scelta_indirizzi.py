from acquisto.carrello import *
from db import connection
import pandas as pd
from accesso.accesso import dati_utente
import sqlalchemy as sa

def acquisto_farmaci() ->None :

    indirizzo_farma :str
    indirizzo_domicilio : str

    print("PROCEDURA DI ACQUISTO")

    #todo diventa una funzione a se stante nome selezione indirizzo
    for prodotto in carrello:

        codice_val = prodotto["codice_farmaco"]
        query = (f" SELECT ricetta FROM FarmaciMagazzino WHERE codice = '{codice_val}' AND ricetta = 'si'")
        serve_ricetta = pd.read_sql_query(query, connection)

        if not serve_ricetta.empty:
            query = (f" SELECT codice FROM FarmaciMagazzino WHERE codice = '{codice_val}' ")
            codicefarmaco= pd.read_sql_query(query,connection)
            if codicefarmaco.empty:
                return None  # o puoi alzare un'eccezione se è obbligatorio
# prendi il primo valore (prima riga, prima colonna) e lo trasformi in stringa
            codicefarmaco = str(codicefarmaco.iloc[0, 0])

            codice_fiscale_utente = dati_utente()
         #   print("CF utente (id_cliente):",codice_fiscale_utente ) per verifica

            query = (f" SELECT codice_farmaco FROM Ricette WHERE codice_farmaco ='{codicefarmaco}' AND UPPER(TRIM(codice_fiscale)) = '{codice_fiscale_utente}'")
            nome_ck = pd.read_sql_query(query,connection)
            if nome_ck.empty :
                print("Non è associata nessuna ricetta per questo farmaco al profilo corrente, il prodotto verrà eliminato dal carrello")
                carrello.remove(prodotto)
        # 1) Vedi cosa c'è in Ricette per quel farmaco
        dbg = pd.read_sql_query(
            sa.text("SELECT codice_farmaco, '['||codice_fiscale||']' as cf FROM Ricette WHERE codice_farmaco = :cod"),
            connection, params={"cod": codice_val}
        )
        print("Ricette per farmaco:", codice_val)
        print(dbg.to_string(index=False))

        # 2) Stampa il CF che stai usando
        print("CF usato:", f"[{codice_fiscale_utente}]")

        if serve_ricetta.empty:
            print("per ricevere l'ordine a domicilio digitare 1")
            print("per ritirare l'ordine nella farmacia assoiata più vicina digitare 2")
            scelta = input()
        elif not serve_ricetta.empty :
            scelta ="2"

        if scelta =="1":
            indirizzo_domicilio= input("Inserire l'indirizzo di domicilio a cui si vuole ricevere l'ordine : ")
        elif scelta == "2":
            print("seleziona una farmacia per il ritiro dei prodotti tra gli indirizzi disponibili")
            print("servizio non disponibile")  # TODO aggiungi tabella indirizzi


