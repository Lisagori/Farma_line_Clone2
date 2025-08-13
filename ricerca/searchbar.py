from db import connection
import pandas as pd
from acquisto.carrello import aggiunta_carrello

def search_bar() -> None:
    medicinale :str
    filtri : str
    aggiungi_carrello :str

    print("BARRA DI RICERCA")
    filtri = input("Vuoi applicare dei filtri alla tua ricerca? (digitare si o no) : ")

    if filtri == "si":
        print("Indica almeno uno dei seguenti filtri, quando non si vuole mettere un filtro premere semplicemente invio")
        indicazioni_terapeutiche = input("Inserire le indicazioni terapeutiche : ")
        composizione = input("Inserire la composizione: ")
        posologia = input("Inserire la posologia : ")

        filters = []  #lista
        if indicazioni_terapeutiche:
            filters.append(f"LOWER(s.indicazioni_terapeutiche) LIKE LOWER ('%{indicazioni_terapeutiche}%')")

        if composizione:
            filters.append(f"LOWER (s.composizione) LIKE LOWER ('%{composizione}%')")

        if posologia:
            filters.append(f"LOWER (s.posologia) LIKE LOWER ('%{posologia}%')")

        query = """
                SELECT 
   
                    f.codice AS codice_farmaco,      -- alias univoco
                    f.nome,
                    f.ricetta,
                    f.preparato_galenico,
                    f.prezzo,
                    f.quantità,
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
                """
        if filters:
            query += " WHERE " + " AND ".join(filters)
            results = pd.read_sql(query, connection)

        else :
            print("Nessun filtro inserito. Ricerca annullata.")
            results = pd.DataFrame() # equivalente a lista vuota

    elif filtri == "no":
        medicinale = input("Digitare il nome del farmaco che si sta cercando: ").strip()

        query = f"""
                SELECT
                    f.codice AS codice_farmaco,      -- alias univoco
                    f.nome,
                    f.ricetta,
                    f.preparato_galenico,
                    f.prezzo,
                    f.quantità,
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
                    WHERE LOWER(TRIM(f.nome)) LIKE LOWER('%{medicinale}%')  -- TRIM dà più tolleranza sugli spazi
                            """
        results = pd.read_sql(query, connection)
    else:
        print("Operazione non valida.")
        results = pd.DataFrame()  # equivalente a lista vuota

    # Stampa dei risultati
    if not results.empty:
        for farmaco in results.to_dict(orient="records"):
            print(farmaco)
        aggiunta_carrello(results)

    if results.empty:
        print("Nessun farmaco trovato.")
        return  # torna al menu precedente