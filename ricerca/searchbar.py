from sqlalchemy.orm import sessionmaker
from ricerca.documentazione_farmaci.base_documenti_medicinali import SchedaTecnicaDB
from ricerca.base_medcinali import FarmaciDB, engine


Session = sessionmaker(bind=engine)
session = Session()

def search_bar() ->None :
    medicinale :str
    filtri : str

    print("BARRA DI RICERCA")
    filtri = input("Vuoi applicare dei filtri alla tua ricerca? (digitare si o no)")
    if filtri == "si" :
        print("indica almeno uno dei seguenti filtri, quando non si vuole mettere un filtro premere semplicemente invio")
        scheda_check = session.query(SchedaTecnicaDB).filter_by(indicazioni_terapeutiche=f"%{input("Inserire le indicazioni terapeutiche : ")}%",
                                                            composizione = f"%{input("Inserire la composizione : ")}%",
                                                            posologia = f"%{input("Inserire la posologia :")}%",
                                                                ).all()

        med_check = session.query(FarmaciDB).filter_by(codice = SchedaTecnicaDB.codice).all()

    elif filtri == "no":
        medicinale = input(" Digitare il nome del farmaco che si sta cercando : ")
        med_check = session.query(FarmaciDB).filter_by(nome = medicinale).all()

    else :
        print("operazione non valida")

    if med_check :
        for med in med_check:
            print(" INFORMAZIONI FARMACO")
            print(med) # fa riferimento alla funzione __repr__ e quindi usa quel tipo di stampa

    else :
        print("nessun farmaco trovato")
