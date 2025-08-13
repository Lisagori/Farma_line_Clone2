import pandas as pd
from sqlalchemy import text

from db import connection


def aggiorna_magazzino() -> None :

    scelta : str
    controllo : bool = False
    verifica : str = "1"

    query = "SELECT codice, nome, quantità FROM FarmaciMagazzino WHERE quantità <= 2 "
    riordinare = pd.read_sql(query, connection)

    if not riordinare.empty:
        print("ATTENZIONE!! I seguenti farmaci stanno per terminare o sono già terminati ")
        for farmaco in riordinare.to_dict(orient="records"):
            print(farmaco)
    else :
        return None

    while not controllo :
        print("Se si vuole aggiornare le quantità dei farmaci sopra elencati digitare 1")
        print("Per procedere con altre operazioni digitare 2")
        scelta = input()

        if scelta == "1" :

            controllo = True
            while verifica =="1" :
                cod = input("Inserire il codice del farmaco che si vuole aggiornare : ")

                query = f"SELECT codice FROM FarmaciMagazzino WHERE codice = '{cod}' AND quantità <= 2 "
                ricerca = pd.read_sql(query, connection)

                if not ricerca.empty :
                    try :
                        new_quantity = int(input("Inserire la quantità aggiornata : "))
                    except ValueError :
                        print("Il valore inserito non è compatibile, riprovare ")

                    query = f"UPDATE FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{cod}'"
                    connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                    connection.commit()

                    print("Se si desidera continuare ad aggiornare le quantità digitare 1 ")
                    print("Per procedere con altre operazioni digitare 2 ")
                    verifica = input()

                else :
                    print("Il codice inserito non è presente nella lista fornita , riprovare ")
                    verifica = "1"

        elif scelta == "2":
            controllo = True

            return None
        else :
            print("Operazione non valida")
            controllo = False
