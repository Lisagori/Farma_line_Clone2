from acquisto.dati_ricetta import *
from acquisto.pagamento import pagare
from db import connection
import pandas as pd

def scelta_indirizzi() ->None :

    indirizzo_domicilio : str
    scelta : str = "exit"
    controllo : int

    controllo = inserimento_dati_ricetta()

    if controllo == 0:
        print("per ricevere l'ordine a domicilio digitare 1")
        print("per ritirare l'ordine nella farmacia fisica 2")
        scelta = input()
    elif controllo > 0:
        scelta = "2"

    if scelta =="1":
        indirizzo_domicilio= input("Inserire l'indirizzo di domicilio a cui si vuole ricevere l'ordine : ")
        print(f"Operazione andata a buon fine, l'ordine sarà spedito presso {indirizzo_domicilio}")
        controllo = pagare(indirizzo_domicilio)
        if not controllo:
            print("Operazione terminata")

    elif scelta == "2":
        print("L'ordine potrà essere ritirato entro 10 giorni presso la nostra sede fisica in Via Univeristà di Santa Marta, 26")
        print("Operazione andata a buon fine")

        controllo = pagare("Via Univeristà di Santa Marta, 26")

        if not controllo:
            print("Operazione terminata")

    else :
        print("operazione non valida ")


