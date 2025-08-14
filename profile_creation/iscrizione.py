from classi.persone.classe_persona import Farmacista, Cliente, Persona,Medico


# sezione di codice dedicata  all'iscrizione da usare nel main

def registrazione_utente() ->bool :
    print("Creazione profilo utente, seguire le istruzioni mostrate di seguito :")

    verifica = False
    pearson : Persona

    print("Se si desidera iscriversi come cliente digitare 1")
    print("Se si desidera iscriversi come farmacista digitare 2 ")
    print("Se si desidera iscriversi come medico digitare 3 ")
    controllo= int(input())

    while not verifica :
        if controllo == 1 :
            pearson = Cliente()
            verifica = True

        elif controllo == 2 :
            pearson = Farmacista()
            verifica = True

        elif controllo == 3 :
            pearson = Medico()
            verifica = True

        else :
            print("opzione non valida riprovare")
            return False

    return pearson.iscriversi()

