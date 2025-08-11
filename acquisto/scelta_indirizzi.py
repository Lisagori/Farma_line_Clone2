from acquisto.carrello import *
from db import connection
import pandas as pd
from accesso.accesso import dati_utente

def acquisto_farmaci() ->None :

    prodotto : Farmaco
    indirizzo_farma :str
    indirizzo_domicilio : str

    print("PROCEDURA DI ACQUISTO")

    #todo diventa una funzione a se stante nome selezione indirizzo
    for prodotto in carrello :
        query = (f" SELECT ricetta FROM FarmaciMagazzino WHERE codice = '{prodotto["codice_farmaco"]}' AND ricetta = '{"si" }'")
        serve_ricetta = pd.read_sql_query(query, connection)

        if not serve_ricetta.empty:
            query = (f" SELECT codice FROM FarmaciMagazzino WHERE codice = '{prodotto["codice_farmaco"]}' ")
            codicefarmaco= pd.read_sql_query(query, connection)
            codice_fiscale_utente = dati_utente()

            query = (f" SELECT codice_farmaco FROM Ricette WHERE codice_farmaco ='{codicefarmaco}' AND codice_fiscale = '{codice_fiscale_utente}'")
            nome_ck = pd.read_sql_query(query, connection)
            # fare tabella con nome farmaco , codice fiscale persona, codice ricetta(chiave)
            if nome_ck.empty :
                print("Non è associata nessuna ricetta per questo farmaco al profilo corrente, il prodotto verrà eliminato dal carrello")
                carrello.remove(prodotto)


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


