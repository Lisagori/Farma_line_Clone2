from profile_creation.iscrizione import registrazione_utente
from accesso.accesso import  accesso_utente
from ricerca.searchbar import search_bar


scelta : str
print("HOME PAGE")
scelta= input("""Se si è in possesso di un profilo utente digitare 1 per accedere al servizio.
Se non si possiede un profilo utente digitare 2 per registrarsi al servizio. 
""")

while scelta == "1" :
    scelta = accesso_utente()
    selezione= input("""Se si desidera ricercare medicinali da acquistare digitare 1.
Se si desidera effetuare un un ordine di un preparato galenico magistrale digitare 2. 
    """)
    while selezione == "1":

        selezione = input("""Se si desidera continuare a ricercare medicinali da acquistare digitare 1
Se si desidera terminare la ricerca e procedere all'acquisto digitare 3""")

if scelta == "2" :
    if registrazione_utente() :
        print("seguire le istruzioni per accedere al servizio")
        accesso_utente()
    else :
        print(" Operazione terminata ")
else :
    print(" Operazione terminata ")