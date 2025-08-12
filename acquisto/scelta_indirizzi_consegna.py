from acquisto.dati_ricetta import *
from db import connection
import pandas as pd
from accesso.accesso import dati_utente

def scelta_indirizzi() ->None :

    indirizzo_farma :str
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
    elif scelta == "2":
        print("seleziona una farmacia per il ritiro dei prodotti tra gli indirizzi disponibili")
        print("servizio non disponibile")  # TODO aggiungi tabella indirizzi
    else :
        print("operazione non valida ")


