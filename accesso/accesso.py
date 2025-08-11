import pandas as pd
from db import connection

username: str

def accesso_utente() -> str:
    global username
    pw: str #pw abbrevviazione per password
    count : int
    controllo: int
    count = 3
    controllo = 3
    #il termice chek viene utilizzato per riferire le variabili di controllo usate per verificare la presenza dell'utente

    print("INSERIMENTO DATI PER ACCESSO")

    #sezione dedicata al controllo del nome utente
    username = input("Inserire il proprio nome utente : ")
    query = f"SELECT * FROM ProfiloUtente WHERE nome_utente = '{username}'"
    username_check = pd.read_sql(query, connection)

    while username_check.empty:
        username = input(f" Il nome utente inserito non appartiente a un utente registarto, riprovare (tentativi rimasti {count}): ")
        query = f"SELECT * FROM ProfiloUtente WHERE nome_utente = '{username}'"
        username_check = pd.read_sql(query, connection)
        count -= 1

        if count == 0 :
            print("se non si è in possesso di un profilo utente già registrato selezionare 2 per iscriversi al servizio")
            print("digitare exit se si vuole terminare le operazioni")
            verify = input()
            return verify #si riconduce al main dove fa la nuova iscrizione

    if count > 0 :

            #sezione dedicata al controllo password
            pw = input ("Inserire la propria password : ")
            query = f"SELECT * FROM ProfiloUtente WHERE password = '{pw}'"
            pw_check = pd.read_sql(query, connection)

            while pw_check.empty :
                controllo -= 1
                if controllo > 0:
                    pw = input(" La password inserita  per questo username è incorretta, riprovare : ")
                    query = f"SELECT * FROM ProfiloUtente WHERE password = '{pw}'"
                    pw_check = pd.read_sql(query, connection)

                elif controllo == 0 :
                    print(f"La password inserita  per questo username è incorretta, tentativi rimasti {controllo}")
                    print(f"Operazione fallita")
                    return "exit"

    return "continua"

def dati_utente() -> str :
    global username
    print(username)
    query = (f"SELECT id_cliente FROM ProfiloUtente WHERE nome_utente ='{username}'")
    codice_utente = pd.read_sql(query, connection)
    codice_utente=pd.DataFrame(codice_utente).to_string(index=False)
    return codice_utente