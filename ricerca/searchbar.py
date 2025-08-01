from sqlalchemy.orm import sessionmaker
from ricerca.documentazione_farmaci.base_documenti_medicinali import SchedaTecnicaDB
from ricerca.base_medcinali import FarmaciDB, engine
from acquisto.classi_acquisto import Farmaco
from sqlalchemy import and_, true

Session = sessionmaker(bind=engine)
session = Session()

def search_bar() -> None:
    medicinale :str
    filtri : str
    aggiungi_carrello :str
    carrello : list[Farmaco]
    farmaco : Farmaco
    from sqlalchemy import and_

    print("BARRA DI RICERCA")
    filtri = input("Vuoi applicare dei filtri alla tua ricerca? (digitare si o no) : ")

    if filtri == "si":
        print(
            "Indica almeno uno dei seguenti filtri, quando non si vuole mettere un filtro premere semplicemente invio")
        indicazioni_terapeutiche = input("Inserire le indicazioni terapeutiche : ")
        composizione = input("Inserire la composizione: ")
        posologia = input("Inserire la posologia : ")

        filters = []  #lista

        if indicazioni_terapeutiche:
            filters.append(SchedaTecnicaDB.indicazioni_terapeutiche.ilike(f"%{indicazioni_terapeutiche}%"))
        if composizione:
            filters.append(SchedaTecnicaDB.composizione.ilike(f"%{composizione}%"))
        if posologia:
            filters.append(SchedaTecnicaDB.posologia.ilike(f"%{posologia}%"))

        if filters:
            results = (
                session.query(FarmaciDB, SchedaTecnicaDB)
                .join(SchedaTecnicaDB, FarmaciDB.codice == SchedaTecnicaDB.codice) #viene usato per stampare solo i farmaci con lo stesso codice in comune
                .filter(*filters) #Usando *filters si apre la lista e si passa gli elementi uno ad uno come argomenti separati
                .all()
            )
        else:
            print("Nessun filtro inserito. Ricerca annullata.")
            results = []

    elif filtri == "no":
        medicinale = input("Digitare il nome del farmaco che si sta cercando: ")

        results = (
            session.query(FarmaciDB, SchedaTecnicaDB)
            .join(SchedaTecnicaDB, FarmaciDB.codice == SchedaTecnicaDB.codice) #viene usato per stampare solo i farmaci con lo stesso codice in comune
            .filter(FarmaciDB.nome.ilike(f"%{medicinale}%")) #filtro parziale (anche lettere maiuscole/minuscole)
            .all()
        )
    else:
        print("Operazione non valida.")
        results = []

    # Stampa dei risultati
    if results:
        for farmaco, scheda in results:
            print("\nINFORMAZIONI FARMACO")
            print(farmaco)
            print("\nSCHEDA TECNICA")
            print(scheda)

        aggiungi_carrello = input(
            "\nDigitare 'si' se si vuole aggiungere il prodotto al carrello, altrimenti digitare 'no': ")
        if aggiungi_carrello == "si":
            print("Azione non disponibile al momento.")
    else:
        print(" Nessun farmaco trovato.")
