from profile_creation.iscrizione import registrazione_utente
from accesso.accesso import  accesso_utente
from ricerca.searchbar import *
from acquisto.classi_acquisto import Farmaco
from db import connection

operazione : str
verifica : bool
opzioni : str
# modifica accesso con il controllo password e i due return exit e continua

print("HOME PAGE")
print("Se si è in possesso di un profilo utente digitare 1 per accedere al servizio.")
print("Se non si possiede un profilo utente digitare 2 per registrarsi al servizio.")
operazione= input()

# Operazioni con scelta di accesso al servizio
while operazione == "1":
    operazione = accesso_utente()  # restituisce continua se l'operazione si è conclusa correttamente ,
                                   # 2 se ci si vuole registare ,
                                   # exit per terminare le operazioni
    if operazione == "2" :
        if registrazione_utente() : # se è vero la registarzione è avvenuta correttamente , altrimenti vengono terminate le operazioni
            operazione = "1" #per poi procedere all'acesso
        else :
            operazione = "exit"

# Operazioni con scelta di registrazione al servizio
while operazione == "2":
    verifica = registrazione_utente()# se è vero la registarzione è avvenuta correttamente , altrimenti vengono terminate le operazioni

    if verifica:
        operazione = accesso_utente()  # restituisce continua se l'operazione si è conclusa correttamente ,
                                       # 2 se ci si vuole registare ,
                                       # exit per terminare le operazioni
    else:
        operazione = "exit"


if operazione =="continua" : # dentro il servizio della farmacia
    #TODO distinzione tra cliente e farmacista bisogna interrogare l abase dati
    print("Se si desidera cercare farmaci digitare 1")
    print("Se si desidera ordinare una preparazione galenica magistrale digitare 2")
    opzioni = input()
    while opzioni == "1":
        search_bar()
        print("Se si desidera continuare a ricercare medicinali da acquistare digitare 1")
        print("Se si desidera terminare la ricerca e procedere all'acquisto digitare 2")
        opzioni = input()

    if opzioni =="2":
        print("operazione non disponibile")
    else:
        print("operazione non disponibile")

else :
    print("Operazione terminata")
