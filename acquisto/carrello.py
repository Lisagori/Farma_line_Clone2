import pandas as pd

from db import connection

carrello: list[dict] = [] #si inserisce fuori dalla funzione per evitare che il carrello si riazzeri ogni volta che viene chiamata da search_bar
quanto_compro : list[int] = []

def aggiunta_carrello(results)->None:

    ck :bool = False
    controllo :bool = False
    verifica : bool = False

    # sezione dedicata al controllo del codice se è presente o meno nell'elenco trovato nella ricerca
    if len(results) > 1: # Se ce più di un farmaco
        while not ck:
            codice_input = input("\nInserire il codice del farmaco che si vuole acquistare: ")

            for prodotto in results.to_dict(orient="records"):
                if codice_input == prodotto["codice_farmaco"] :
                    verifica = True
                    break
                else :
                    verifica = False

            if not verifica :
                print("Il codice inserito non è valido")
            else:
                ck = True
    else:# Se ce n'è solo uno
        codice_input =(results.iloc[0]["codice_farmaco"])

    #sezione di codice per controllare che la quantità che si vuole acquistare sia disponibile


    while not controllo :
        ck = False
        while not ck :
            try :
                quantity = int(input("Inserire la quantità di prodotto che si vuole aqcuistare : "))
                ck = True
            except ValueError :
                print("il valore inserito non è compatibile, riprovare")

        query = f"SELECT quantità FROM FarmaciMagazzino WHERE quantità < '{quantity}' AND codice = '{codice_input}' "
        q_trovato = pd.read_sql(query, connection)

        if q_trovato.empty :
            aggiungi_carrello = input("\nDigitare 'si' se si vuole aggiungere il prodotto al carrello, altrimenti digitare 'no': ")
            quanto_compro.append(quantity)

            if aggiungi_carrello == "si":
                # results: DataFrame con almeno la colonna "codice"

                riga = results.loc[results["codice_farmaco"] == codice_input]

                if not riga.empty:
                    farmaco_dict = riga.iloc[0].to_dict()  # prendo la prima corrispondenza
                    carrello.append(farmaco_dict)
                    print("Farmaco aggiunto al carrello.")
                else:
                    print("Codice non trovato tra i risultati mostrati.")

                print("Contenuto attuale del carrello:")

                if carrello:
                    for prodotto in carrello :
                        print(f" codice : {prodotto["codice_farmaco"]} ")
                        print(f" nome : {prodotto["nome"]} ")
                        print(f" quantità : {quantity} ")
                        print(f" prezzo : {quantity*prodotto["prezzo"]}")
                else:
                    print("Il carrello è vuoto.")

            elif aggiungi_carrello == "no":
                print("Farmaco non aggiunto al carrello")
                print("Contenuto attuale del carrello:")

                if carrello:
                    print(pd.DataFrame(carrello).to_string(index=False))
                else:
                    print("Il carrello è vuoto.")
            else:
                print("Operazione non valida.")

            controllo = True
        else :
            if q_trovato.iloc[0,0] == 0 :
                print("Il prodotto è terminato non è possibile acquistarlo")
                controllo = True
            else :
                print("La quantità di farmaco in magazzino non è sufficiente, riprovare  ")
