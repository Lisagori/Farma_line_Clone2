from profile_creation.base_iscrizione import ProfiloUtenteDB, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def accesso_utente() -> str:
    username :str
    pw : str #pw abbrevviazione per password
    count : int
    count = 3

    #il termice chek viene utilizzato per riferire le variabili di controllo usate per verificare la presenza dell'utente

    #sezione dedicata al controllo del nome utente
    username = input("Inserire il proprio nome utente : ")
    username_check = session.query(ProfiloUtenteDB).filter_by(nome_utente=username).first()
    while not username_check  :
        username = input(f" Il nome utente inserito non appartiente a un utente registarto, riprovare (tentativi rimasti {count}): ")
        username_check  = session.query(ProfiloUtenteDB).filter_by(nome_utente=username).first()
        count -= 1
        if count == 0 :
            print("se non si è in possesso di un profilo utente già registrato selezionare 2 per iscriversi al servizio")
            print("digitare exit se si vuole terminare le operazioni")
            verify = input()
            return verify#si riconduce al main dove fa la nuova iscrizione

    if count > 0 :
            #sezione dedicata al controllo password
            pw = input ("Inserire la propria password : ")
            pw_check = session.query(ProfiloUtenteDB).filter_by(nome_utente=username, password = pw).first()
            while not pw_check :
                pw = input(" La password inserita  per questo username è incorretta, riprovare : ")
                pw_check = session.query(ProfiloUtenteDB).filter_by(nome_utente=username, password = pw).first()


