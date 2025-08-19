from classi.persone.classe_persona import Farmacista, Cliente, Persona, Medico, LavoratoreSanitario


# sezione di codice dedicata  all'iscrizione da usare nel main

def registrazione_utente() ->bool :
    print("Creazione profilo utente, seguire le istruzioni mostrate di seguito :")

    verifica: bool = False
    pearson : Persona

    while not verifica:

        print("Se si desidera iscriversi come cliente digitare 1")
        print("Se si desidera iscriversi come farmacista digitare 2 ")
        print("Se si desidera iscriversi come medico digitare 3 ")
        controllo= input()

        if controllo == '1' :
            pearson = Cliente()
            break

        elif controllo == '2' :
            pearson = LavoratoreSanitario("farmacista")
            break

        elif controllo == '3' :
            pearson = LavoratoreSanitario("medico")
            break

        else :
            print("opzione non valida riprovare")

    return pearson.iscriversi()

