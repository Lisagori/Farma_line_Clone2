from classi.persone.classe_persona import ProfiloUtente, ProfiloFarmacista, ProfiloMedico, ProfiloCliente
from db import connection
import pandas as pd

username: str


def accesso_utente() -> str:
    global username

    pw: str  # pw abbrevviazione per password
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
                    pw = input(f" La password inserita  per questo username è incorretta, riprovare (tentetivi rimasti {controllo}): ")
                    query = f"SELECT * FROM ProfiloUtente WHERE password = '{pw}'"
                    pw_check = pd.read_sql(query, connection)

                elif controllo == 0 :
                    print(f"La password inserita  per questo username è incorretta, tentativi rimasti {controllo}")
                    print(f"Operazione fallita")
                    return "exit"

    return "continua"

def get_profilo() -> ProfiloUtente:

    global username

    query = f"SELECT password, tipo_profilo FROM ProfiloUtente WHERE nome_utente = '{username}'"
    profile = pd.read_sql_query(query, connection)

    pw = str(profile.iloc[0, 0])
    tipo_prof = str(profile.iloc[0,1])

    if tipo_prof == "cliente" :
        query = f"SELECT id_cliente FROM ProfiloUtente WHERE nome_utente = '{username}'"
        id_c = pd.read_sql_query(query, connection)
        id_c = str(id_c.iloc[0,0])

        profilo = ProfiloCliente(username,pw, id_c, tipo_prof)

    elif tipo_prof == "farmacista":
        query = f"SELECT id_sanitari FROM ProfiloUtente WHERE nome_utente = '{username}'"
        id_f = pd.read_sql_query(query, connection)
        id_f = str(id_f.iloc[0,0])
        profilo = ProfiloFarmacista(username,pw, id_f, tipo_prof)
    elif tipo_prof == "medico":
        query = f"SELECT id_sanitari FROM ProfiloUtente WHERE nome_utente = '{username}'"
        id_m = pd.read_sql_query(query, connection)
        id_m = str(id_m.iloc[0, 0])
        profilo = ProfiloMedico(username, pw, id_m, tipo_prof)
    else :
        print("Operazione fallita")

    return profilo