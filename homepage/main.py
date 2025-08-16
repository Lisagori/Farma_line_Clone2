from classi.persone.classe_persona import ProfiloUtente, ProfiloCliente, ProfiloFarmacista, ProfiloMedico
from profile_creation.iscrizione import registrazione_utente
from accesso.accesso import accesso_utente, get_profilo
from db import connection


operazione : str
verifica : bool
opzioni : str = "1"
controllo : bool
profilo : ProfiloUtente

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

    profilo = get_profilo() #recupera il profilo dell'utente che ha appena eseguito l'accesso

    # sezione dedicata al cliente
    if  isinstance(profilo , ProfiloCliente):

        while opzioni == "1":
            profilo.search_bar()
            print("Se si desidera continuare a ricercare medicinali da acquistare digitare 1")
            print("Se si desidera terminare la ricerca e procedere all'acquisto digitare 2")
            opzioni = input()

        if opzioni == "2":
            print("PROCEDURA DI ACQUISTO")
            profilo.scelta_indirizzi()

        else:
            print("operazione non disponibile")

    # sezione dedicata al farmacista
    elif isinstance(profilo , ProfiloFarmacista) :

        profilo.aggiorna_magazzino()

        print("Se si desidera aggiungere nuovi farmaci al magazzino digitare 1")
        print("Per verificare l'esistenza dell'ordine e confermare l'avvenuta consegna digitare 2")
        opzioni = input()

        if opzioni == "1":
            print("PROCEDURA DI AGGIUNTA FARMACI")
            profilo.aggiunta_farmaci()

        elif opzioni == "2":
            print("PROCEDURA DI VERIFICA")
            profilo.verifica_ordine()

        else:
            print("operazione inesistente")

    #sezione dedicata al medico
    elif isinstance(profilo , ProfiloMedico):
        print("PROCEDURA DI PRESCRIZIONE RICETTA MEDICA")
        profilo.crea_ricetta()

    else:
        print("Operazione non valida")
else :
    print("Operazione terminata")
#TODO aggiungere gli exept
