from sqlalchemy.orm import sessionmaker
from ricerca.documentazione_farmaci.base_documenti_medicinali import SchedaTecnicaDB
from ricerca.base_medcinali import FarmaciDB, engine
from acquisto.classi_acquisto import Farmaco
from sqlalchemy import text

Session = sessionmaker(bind=engine)
session = Session()

def search_bar() -> None:
    medicinale :str
    filtri : str
    aggiungi_carrello :str
    carrello : list[Farmaco]
    farmaco : Farmaco

    print("BARRA DI RICERCA")
    filtri = input("Vuoi applicare dei filtri alla tua ricerca? (digitare si o no) : ")
    if filtri == "si" :
        print("indica almeno uno dei seguenti filtri, quando non si vuole mettere un filtro premere semplicemente invio")
        scheda_check = session.query(SchedaTecnicaDB).filter_by(indicazioni_terapeutiche=f"%{input("Inserire le indicazioni terapeutiche : ")}%",
                                                            composizione = f"%{input("Inserire la composizione : ")}%",
                                                            posologia = f"%{input("Inserire la posologia :")}%",
                                                                ).all()

        med_check = session.query(FarmaciDB).filter_by(codice = SchedaTecnicaDB.codice).all()

    elif filtri == "no":
        medicinale = input(" Digitare il nome del farmaco che si sta cercando : ")
        med_check = session.query(FarmaciDB).filter_by(nome = f"%{medicinale}%").all()
        scheda_check = session.query(SchedaTecnicaDB).filter_by(codice =FarmaciDB.codice).all()

    else :
        print("operazione non valida")

    if med_check :
        for med in med_check :
            print(" INFORMAZIONI FARMACO")
            print(med) # fa riferimento alla funzione __repr__ e quindi usa quel tipo di stampa
            for scheda in scheda_check :
                print(" SCHEDA TECNICA ")
                print(scheda)

        aggiungi_carrello= input("Digitare si se si vuole aggiungere il prodotto al carrello , altrimenti digitare no : ")
        if aggiungi_carrello =="si" :
            print("azione non disponibile ")
    else :
        print("nessun farmaco trovato")
