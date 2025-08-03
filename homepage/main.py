from profile_creation.iscrizione import registrazione_utente
from accesso.accesso import  accesso_utente
from ricerca.searchbar import *
from acquisto.classi_acquisto import Farmaco

scelta : str
carrello : list[Farmaco] #non utile al momento
scelta2 :str
scelta2 = "1"

print("HOME PAGE")


while scelta2 =="1" :

    scelta = input("""Se si è in possesso di un profilo utente digitare 1 per accedere al servizio.
Se non si possiede un profilo utente digitare 2 per registrarsi al servizio. 
        """)

    while scelta == "1" :
            scelta = accesso_utente()
            selezione= input("""Se si desidera ricercare medicinali da acquistare digitare 1.
Se si desidera effetuare un ordine di un preparato galenico magistrale digitare 2. 
            """)
            while selezione == "1":
                search_bar()
                selezione = input("""Se si desidera continuare a ricercare medicinali da acquistare digitare 1 
Se si desidera terminare la ricerca e procedere all'acquisto digitare 3
""")

            if selezione == "3" :
                # processo di acquisto
                print("Sezione non disponibile ")
                #processo di acquisto
            else:
                print("Inserimento non corretto")

    scelta2 = "2"

    if scelta == "2" :
        if registrazione_utente() :
            scelta2 = "1"
        else :
            print(" Operazione terminata ")
    else :
        print(" Operazione terminata ")