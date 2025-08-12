import random
import pandas as pd
from accesso.accesso import codice_utente
from db import connection


def associa_numero_ordine(indirizzo:str)->None :

    num_ordine : int

    num_ordine = random.randint(0, 1000000000)
    print(f"Fornire il seguente codice al momento del ritiro : {num_ordine}")

    codice_fiscale_utente = codice_utente()

    new_ordine = pd.DataFrame(
        [[
            num_ordine,
            codice_fiscale_utente,
            indirizzo,
        ]],
        columns=[
            'numero_ordine',  # <-- niente spazio finale
            'cf',
            'indirizzo',
        ]
    )
    new_ordine.to_sql('Ordine', connection, if_exists='append', index=False)
    connection.commit()