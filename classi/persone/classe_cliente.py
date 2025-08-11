import pandas as pd
from db import connection
from classi.persone.classe_persona import Persona
from classi.documenti.classe_tessera_sanitaria import TesseraSanitaria

class Cliente(Persona):
    t_s: TesseraSanitaria #t_s abbreviazione tessera sanitaria

    def __init__(self):
        super().__init__()
        self.t_s = TesseraSanitaria()

    def iscriversi(self) -> bool:
        query = f"SELECT * FROM Clienti WHERE codice_fiscale = '{self.t_s.codice_fiscale}'"
        cliente = pd.read_sql(query, connection)
        if not cliente.empty: # è un dataframe
            print("Il codice fiscale inserito appartiene a un utente già registrato")

            print("Se si vuole accedere al servizio digitare 1")
            print("Se si vuole ritentare il processo di iscrizione digitare 2")
            print("Digitare exit se si vuole terminare l'operazione")
            scelta = input()

            if scelta == "1":
                return True
            elif scelta == "2":
                self.t_s.codice_fiscale = input("Inserire il codice fiscale corretto : ")
                return self.iscriversi()
            else:
                return False

        else:
            self.t_s.associazione_tessera_a_db()
            new_cliente = pd.DataFrame(
                columns=['nome','cognome','codice_fiscale'],
                data=[
                [self.nome, self.cognome, self.t_s.codice_fiscale ]
                ]
            )
            new_cliente.to_sql('Clienti', connection, if_exists='append', index=False)
            connection.commit()
            #sezione per associazione profilo utente
            return self.crea_profilo()