from profile_creation.base_iscrizione import ProfiloUtenteDB, engine
from profile_creation.classi_iscrizione import session

def accesso_utente() -> None:
    username :str
    pw : str #pw abbrevviazione per password

    #il termice chek viene utilizzato per riferire le variabili di controllo usate per verificare la presenza dell'utente
    username = input("Inserire il proprio nome utente : ")
    username_check = session.query(ProfiloUtenteDB).filter_by(nome_utente=username).first()
    while not username_check  :
        username = input(" Il nome utente inserito non appartiente a un utente registarto, riprovare : ")
        username_check  = session.query(ProfiloUtenteDB).filter_by(nome_utente=username).first()

    pw = input ("Inserire la propria password : ")
    pw_check = session.query(ProfiloUtenteDB).filter_by(nome_utente=username, password = pw).first()
    while not pw_check :
        pw = input(" La password inserita  per questo username è incorretta, riprovare : ")
        pw_check = session.query(ProfiloUtenteDB).filter_by(nome_utente=username, password = pw).first()


