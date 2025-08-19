from funzioni_generali.controlli_function import controlla, check_se_vuoto
from datetime import datetime
from db import connection
import pandas as pd


class TesseraSanitaria :

    codice_fiscale: str
    sesso: str
    luogo_nascita: str
    provincia: str
    data_nascita: datetime.date
    data_scadenza: datetime.date
    numero_identificazione_tessera: str

    def __init__(self):

        ck: bool =False
        print( " Di seguito si inseriscano i dati della tessera sanitaria : ")
        self.codice_fiscale = controlla(" CODICE FISCALE :", 16) # nel codice fiscale si contano 16 caratteri alfanumerici
        self.sesso = controlla(" SESSO : ", 1)
        self.luogo_nascita = check_se_vuoto(" LUOGO DI NASCITA : ")
        self.provincia = controlla(" PROVINCIA : ", 2)
        #controllo che la data di nascita sia inserita correttamente
        while not ck:
            data_input = controlla(" DATA DI NASCITA (gg/mm/aaaa) : ", 10)
            try:
                self.data_nascita = datetime.strptime(data_input, "%d/%m/%Y").date()
                ck=True
            except ValueError:
                print("Data non valida!")
                ck=False
        #controllo che la data di scadenza sia inserita correttamente
        ck= False
        while not ck:
            data_input = controlla(" DATA DI SCADENZA (gg/mm/aaaa) : ", 10)
            try:
                self.data_scadenza = datetime.strptime(data_input, "%d/%m/%Y").date()
                ck = True
            except ValueError:
                print("Data non valida!")
                ck=False
        self.numero_identificazione_tessera = controlla(" NUMERO IDENTIFICAZIONE TESSERA : ", 20)# sulla tessera sanitaria fisica sono 20 caratteri alfanumerici

    def associazione_tessera_a_db(self)->None:
        new_tessera = pd.DataFrame(
            [[
                self.codice_fiscale,
                self.sesso,
                self.luogo_nascita,
                self.provincia,
                self.data_nascita,
                self.data_scadenza,
                self.numero_identificazione_tessera
            ]],
            columns=[
                'codice_fiscale',  # <-- niente spazio finale
                'sesso',
                'luogo_nascita',
                'provincia',
                'data_nascita',
                'data_scadenza',
                'numero_identificazione_tessera'
            ]
        )
        new_tessera.to_sql('TesseraSanitaria', connection, if_exists='append', index=False)
        connection.commit()