import pandas as pd
from db import connection
from classi.persone.classe_persona import Persona
from classi.documenti.classe_tesserino_professionale import TesserinoProfessionale

class Farmacista(Persona):
    t_p: TesserinoProfessionale #t_p abbreviazione tesserino professionale

    def __init__(self):
        super().__init__()
        self.t_p = TesserinoProfessionale("farmacista")

    def iscriversi(self) ->bool :
        query = f"SELECT * FROM Farmacista WHERE matricola = '{self.t_p.n_matricola}'"
        farmacista = pd.read_sql(query, connection)
        # si definisce la ricerca da database per controllare se la persona è già registrata
        if not farmacista.empty: #è un dataframe
            print("La matricola inserita appartiene a un utente già registrato")

            print("Se si vuole accedere al servizio digitare 1")
            print("Se si vuole ritentare il processo di iscrizione digitare 2")
            print("Digitare exit se si vuole terminare l'operazione")
            scelta = input()

            if scelta == "1":
                return True
            elif scelta == "2":
                self.t_p.n_matricola = input("Inserire il numero di matricola corretto : ")
                return self.iscriversi()
            else:
                return False

        else:
            self.t_p.associazione_tessera_a_db()
            new_farmacista = pd.DataFrame(
                columns=['nome','cognome','matricola'],
                data=[
                [self.nome, self.cognome, self.t_p.n_matricola]
                ]
            )
            new_farmacista.to_sql('Farmacista', connection, if_exists='append', index=False)
            connection.commit()
            # sezione per associazione profilo utente
            return self.crea_profilo()