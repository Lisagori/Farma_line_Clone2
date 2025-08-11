from classi.persone.classe_persona import Persona
import pandas as pd
from db import connection
from classi.persone.classe_cliente import Cliente
from classi.persone.classe_farmacista import Farmacista

class ProfiloUtente :
    nome_utente:str
    password: str
    utente: Persona

    def __init__(self,user : Persona):
        self.utente = user
        self.nome_utente = input(" inserire un nome utente : ") # inserire controllo per corrispondenza profilo utente
        self.password = input(" inserire una password : ")

    def associazione_profilo_utente(self) -> None:

        if isinstance(self.utente, Cliente):
            new_profile= pd.DataFrame ( # prf fa riferimento al profilo utente da associare alla relativa tebella
                    columns=['nome_utente','password','id_cliente'],
                data= [
                    [self.nome_utente,self.password,self.utente.t_s.codice_fiscale]
                ]
            )
            new_profile.to_sql('ProfiloUtente', connection, if_exists='append', index=False)
            connection.commit()

        elif isinstance(self.utente, Farmacista):
            new_profile = pd.DataFrame(  # prf fa riferimento al profilo utente da associare alla relativa tebella
                columns=['nome_utente','password','id_farmacista'],
                data=[
                [self.nome_utente, self.password, self.utente.t_p.n_matricola]
                ]
            )
            new_profile.to_sql('ProfiloUtente', connection, if_exists='append', index=False)
            connection.commit()
        else:
            print("  Associazione profilo fallita: tipo utente non valido.")
            return #TODO CONTROLLARE COSA RESTITUISCE

        print("Profilo utente aggiunto con successo.")
        return None

    def controllo_utente(self)->bool:
        query = f"SELECT * FROM ProfiloUtente WHERE nome_utente = '{self.nome_utente}'"
        profilo_esistente = pd.read_sql(query, connection)
        if not profilo_esistente.empty: #pd.read_sql(...) restituisce sempre un DataFrame di pandas.
            print(f"Il nome utente '{self.nome_utente}' è già in uso. Scegliere un altro nome.")
            return False
        else:
            return True