from acquisto.dati_ricetta import *
from db import connection
import pandas as pd

def scelta_indirizzi() ->None :

    indirizzo_domicilio : str
    scelta : str = "exit"
    controllo : int

    controllo = inserimento_dati_ricetta()

    if controllo == 0:
        print("per ricevere l'ordine a domicilio digitare 1")
        print("per ritirare l'ordine nella farmacia assoiata più vicina digitare 2")
        scelta = input()
    elif controllo > 0:
        scelta = "2"

    if scelta =="1":
        indirizzo_domicilio= input("Inserire l'indirizzo di domicilio a cui si vuole ricevere l'ordine : ")
        print(f"Operazione andata a buon fine, l'ordine sarà spedito presso {indirizzo_domicilio}")
    elif scelta == "2":
        print("seleziona una farmacia per il ritiro dei prodotti tra gli indirizzi disponibili")
        query = "SELECT * FROM IndirizziFarmacia "
        indirizzi = pd.read_sql_query(query, connection)

        for indirizzo in indirizzi.to_dict(orient="records"):#stampa indirizzi
            print(indirizzo)

        codice_farma = input("Inserire il codice della farmacia in cui si vuole ritirare l'ordine ")
        query = f"SELECT nome_farmacia, città, via, numero_civico FROM IndirizziFarmacia WHERE codice_farmacia = '{codice_farma}'"
        farma = pd.read_sql_query(query, connection)

        print(f"Operazione andata a buon fine, l'ordine potrà essere ritirato presso")
        print(str(farma.iloc[0]))

    else :
        print("operazione non valida ")


