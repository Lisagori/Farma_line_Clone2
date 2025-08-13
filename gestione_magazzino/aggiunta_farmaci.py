import pandas as pd
from db import connection
from funzioni_generali.controlla import  check_se_vuoto


def aggiunta_farmaci() -> None :

    ck : bool =False
    nome :str
    ricetta :str
    preparato_galenico :str
    quanto : int
    prezzo: float

    print("Per aggiungere una nuova tipologia di medicinale in magazzino, seguire le istruzioni di seguito riportate ")

    query = "SELECT MAX(codice) FROM FarmaciMagazzino"
    cod = pd.read_sql(query, connection)

    nome = check_se_vuoto("Inserire il nome del farmaco : ")
    ricetta = check_se_vuoto("Il farmaco necessita di ricetta ? (digitare si o no) : ")
    preparato_galenico = check_se_vuoto("È un preparato galenico ? (digitare si o no) : " )

    while not ck:
        try:
            quanto = int(check_se_vuoto("Inserire la quantità di farmaco che si vuole aggiungere in magazzino : "))
            ck = True
        except ValueError:
            print("Il valore inserito non è compatibile, riprovare")

    ck = False
    while not ck:
        try:
            prezzo = float(input("Inserire il prezzo del prodotto in euro ( 0.00 ): "))
            ck = True
        except ValueError:
            print("Il valore inserito non è compatibile, riprovare")

    indicazioni_terapeutiche = check_se_vuoto(" Inserire le idicazioni terapeutiche : ")
    composizione = check_se_vuoto("Inserire i componenti del farmaco : ")
    eccipienti = check_se_vuoto("Inserire gli eccipienti del farmaco : ")
    controindicazioni = check_se_vuoto("Inserire le controindicazioni : ")
    posologia= check_se_vuoto("Inserire la posologia : ")
    avvertenze = check_se_vuoto("Inserire le avvertenze : ")
    effetti_indesiderati = check_se_vuoto("Inserire gli effetti indesiderati : ")

    cod = int(str(cod.iloc[0,0])) +1

    # sezione per aggiornare la tabella di SchedaTecnica sul database
    new_scheda = pd.DataFrame(
        [[
            cod,
            indicazioni_terapeutiche,
            composizione,
            eccipienti,
            controindicazioni,
            posologia,
            avvertenze,
            effetti_indesiderati
        ]],
        columns=[
            'codice',  # <-- niente spazio finale
            'indicazioni_terapeutiche',
            'composizione',
            'eccipienti',
            'controindicazioni',
            'posologia',
            'avvertenze',
            'effetti_indesiderati'
        ]
    )
    new_scheda.to_sql('SchedaTecnica', connection, if_exists='append', index=False)

    # sezione per aggiornare la tabella di FarmaciMagazzino sul database
    new_farmaco = pd.DataFrame(
        [[
            nome,
            ricetta,
            preparato_galenico,
            prezzo,
            quanto,
            cod
        ]],
        columns=[
            'nome',  # <-- niente spazio finale
            'ricetta',
            'preparato_galenico',
            'prezzo',
            'quantità',
            'codice'
        ]
    )
    new_farmaco.to_sql('FarmaciMagazzino', connection, if_exists='append', index=False)

    connection.commit()
