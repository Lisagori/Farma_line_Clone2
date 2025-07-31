from profile_creation.iscrizione import registrazione_utente
from accesso.accesso import  accesso_utente

print("HOME PAGE")
scelta= int(input("""Se si è in possesso di un profilo utente digitare 1 per accedere al servizio.
Se non si possiede un profilo utente digitare 2 per registrarsi al servizio. 
"""))

if scelta == 1 :
    accesso_utente()

elif scelta ==2 :
    if registrazione_utente() :
        print("seguire le istruzioni per accedere al servizio")
        accesso_utente()
    else :
        print(" Operazione terminata ")