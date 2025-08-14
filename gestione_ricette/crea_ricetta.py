import string
import pandas as pd
from accesso.accesso import get_nome_utente
from db import connection
from funzioni_generali.altro import create_random_string


def crea_ricetta() -> None:

    cod : str
    i : int

    print("Digitare il codice del farmaco che si vuole prescrivere, selezionando dal segunete elenco ")

    query = "SELECT codice , nome FROM FarmaciMagazzino WHERE ricetta = 'si' "
    elenco = pd.read_sql(query, connection)

    if not elenco.empty:
        for farmaco in elenco.to_dict(orient="records"):
            print(farmaco)
    else :
        print ("Non ci sono farmaci con ricetta da poter prescrivere in magazzino")


    cod_farmaco = input()
    cod_fisc = input("Inserire il codice fiscale del paziente a cui si sta prescrivendo il farmaco : ")

    cod_ricetta = ((create_random_string(4, string.digits)
                + create_random_string(1, string.ascii_uppercase))
                +' '
                + create_random_string(10, string.digits))

    nome_med = get_nome_utente()

    new_ricetta = pd.DataFrame(
            [[
                cod_ricetta,
                cod_fisc,
                cod_farmaco,
                nome_med
            ]],
            columns=[
                'codice_ricetta',  # <-- niente spazio finale
                'codice_fiscale',
                'codice_farmaco',
                'nome_medico'
            ]
        )
    new_ricetta.to_sql('Ricetta', connection, if_exists='append', index=False)
    connection.commit()

    print(f"Codice ricetta : {cod_ricetta}")

