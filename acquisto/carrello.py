from classi.farmaci.classe_farmaci import Farmaco
import pandas as pd

carrello: list[Farmaco] = [] #si inserisce fuori dalla funzione per evitare che il carrello si riazzeri ogni volta che viene chiamata da search_bar

def aggiunta_carrello(results)->None:

    if len(results) > 1: # Se ce più di un farmaco
        codice_input = (input("\nInserire il codice del farmaco che si vuole acquistare: "))
    else:# Se ce n'è solo uno
        codice_input =(results.iloc[0]["codice_farmaco"])

    aggiungi_carrello = input("\nDigitare 'si' se si vuole aggiungere il prodotto al carrello, altrimenti digitare 'no': ")

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
            print(pd.DataFrame(carrello).to_string(index=False))
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