from profile_creation.iscrizione import registrazione_utente
from accesso.accesso import  accesso_utente

print("HOME PAGE")

controll ="go"
print( "Se si vuole terminare scrivere exit quando richiesto ")
while controll != "exit" :
    registrazione_utente()
    controll = input("Vuoi continuare ?  ")
