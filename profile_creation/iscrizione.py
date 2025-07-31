from profile_creation.classi_iscrizione import *

# sezione di codice dedicata  all'iscrizione da usare nel main

def registrazione_utente() ->bool :
    print("Creazione profilo utente, seguire le istruzioni mostrate di seguito :")

    verifica = False
    pearson : Persona
    controllo= int(input("""Se si desidera iscriversi come cliente digitare 1
Se si desidera iscriversi come farmacista digitare 2 
    """))
    while not verifica :
        if controllo == 1 :
            pearson = Cliente()
            verifica = True

        elif controllo == 2 :
            pearson = Farmacista()
            verifica = True
        else :
            print("opzione non valida riprovare")

    return pearson.iscriversi()
