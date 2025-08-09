from acquisto.classi_acquisto import Farmaco
from db import connection
import pandas as pd

carrello : list[Farmaco]=[]

def search_bar() -> None:
    medicinale :str
    filtri : str
    aggiungi_carrello :str

    farmaco : Farmaco

    print("BARRA DI RICERCA")
    filtri = input("Vuoi applicare dei filtri alla tua ricerca? (digitare si o no) : ")

    if filtri == "si":
        print(
            "Indica almeno uno dei seguenti filtri, quando non si vuole mettere un filtro premere semplicemente invio")
        indicazioni_terapeutiche = input("Inserire le indicazioni terapeutiche : ")
        composizione = input("Inserire la composizione: ")
        posologia = input("Inserire la posologia : ")

        filters = []  #lista
        params = {}

        if indicazioni_terapeutiche:
            filters.append("LOWER(s.indicazioni_terapeutiche) LIKE LOWER(:indicazioni)")
            params["indicazioni"] = f"%{indicazioni_terapeutiche}%"

        if composizione:
            filters.append("LOWER (s.composizione) LIKE LOWER (:composizione)")
            params["composizione"] = f"%{composizione}%"

        if posologia:
            filters.append("LOWER (s.posologia) LIKE LOWER (:posologia)")
            params["posologia"] = f"%{posologia}%"

        query = """
                SELECT 
   
                    f.codice AS codice_farmaco,      -- alias univoco
                    f.nome,
                    f.ricetta,
                    f.preparato_galenico,
                    f.prezzo,
                    s.indicazioni_terapeutiche,
                    s.composizione,
                    s.eccipienti,
                    s.controindicazioni,
                    s.posologia,
                    s.avvertenze,
                    s.effetti_indesiderati
                FROM FarmaciMagazzino AS f
                LEFT JOIN SchedaTecnica AS s
                  ON f.codice = s.codice 
                """
        if filters:
            query += " WHERE " + " AND ".join(filters)
            results = pd.read_sql(query, connection, params=params)

        else :
            print("Nessun filtro inserito. Ricerca annullata.")
            results = pd.DataFrame() # equivalente a lista vuota

    elif filtri == "no":
        medicinale = input("Digitare il nome del farmaco che si sta cercando: ").strip()

        query = """
                SELECT
                    f.codice AS codice_farmaco,      -- alias univoco
                    f.nome,
                    f.ricetta,
                    f.preparato_galenico,
                    f.prezzo,
                    s.indicazioni_terapeutiche,
                    s.composizione,
                    s.eccipienti,
                    s.controindicazioni,
                    s.posologia,
                    s.avvertenze,
                    s.effetti_indesiderati
                FROM FarmaciMagazzino AS f
                JOIN SchedaTecnica AS s
                  ON f.codice = s.codice
                    WHERE LOWER(TRIM(f.nome)) LIKE LOWER(:nome)  -- TRIM dà più tolleranza sugli spazi
                            """
        params = {"nome": f"%{medicinale}%"}
        results = pd.read_sql_query(query, connection, params=params)
    else:
        print("Operazione non valida.")
        results = pd.DataFrame()  # equivalente a lista vuota

    # Stampa dei risultati
    if not results.empty:
        for farmaco in results.to_dict(orient="records"):
            print(farmaco)

        if len(results) > 1:
            codice_input = int(input("\nInserire il codice del farmaco che si vuole acquistare: "))
        else:# Se ce n'è solo uno
            codice_input =int(results.iloc[0]["codice_farmaco"])

        aggiungi_carrello = input(
            "\nDigitare 'si' se si vuole aggiungere il prodotto al carrello, altrimenti digitare 'no': ")
        if aggiungi_carrello == "si":
            # results: DataFrame con almeno la colonna "codice"
            try:
                codice_input = int(codice_input)
            except ValueError:
                print("Codice non valido.")
                return

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

    if results.empty:
        print("Nessun farmaco trovato.")
        return  # torna al menu precedente