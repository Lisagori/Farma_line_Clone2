from funzioni_generali.controlli_function import controlla
from db import connection
import pandas as pd


class TesseraSanitaria :
    codice_fiscale: str
    sesso: str
    luogo_nascita: str
    provincia: str
    data_nascita: str
    data_scadenza: str
    numero_identificazione_tessera: str

    #TODO quando possibile inserire controllo data di nascita e scadenza tessera sanitaria

    def __init__(self):

        print( " Di seguito si inseriscano i dati della tessera sanitaria : ")
        self.codice_fiscale = controlla(" CODICE FISCALE :", 16) # nel codice fiscale si contano 16 caratteri alfanumerici
        self.sesso = controlla(" SESSO : ", 1)
        self.luogo_nascita = input(" LUOGO DI NASCITA : ")
        self.provincia = controlla(" PROVINCIA : ", 2)
        self.data_nascita = controlla(" DATA DI NASCITA (gg/mm/aaaa) : ", 10)
        self.data_scadenza = controlla(" DATA DI SCADENZA (gg/mm/aaaa) : ", 10)
        self.numero_identificazione_tessera = controlla(" NUMERO IDENTIFICAZIONE TESSERA : ", 20)# sulla tessera sanitaria fisica sono 20 caratteri alfanumerici


    def associazione_tessera_a_db(self):
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