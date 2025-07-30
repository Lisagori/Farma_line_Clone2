from profile_creation.iscrizioni import registrazione_utente

controll ="go"
print( "Se si vuole terminare scrivere exit quando richiesto ")
while controll != "exit" :
    registrazione_utente()
    controll = input("Vuoi continuare ?  ")
