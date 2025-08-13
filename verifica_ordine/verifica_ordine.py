import pandas as pd
from sqlalchemy import text

from db import connection, engine
from funzioni_generali.controlla import check_se_vuoto


def verifica_ordine()-> None :

    cod_fisc:str
    n_ordine :str
    count : int = 3

    print("RICERCA ORDINE NEL DATABASE")

    cod_fisc = check_se_vuoto("Inserire il codice fiscale del cliente : ")
    n_ordine = check_se_vuoto("Inserire il numero dell'ordine : ")

    query = f"SELECT * FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
    trovato = pd.read_sql(query, connection)

    while trovato.empty :

        print(f"Ordine non trovato, riprovare (tentativi rimasti {count}")
        cod_fisc = check_se_vuoto("Inserire il codice fiscale del cliente : ")
        n_ordine = check_se_vuoto("Inserire il numero dell'ordine : ")

        query = f"SELECT * FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
        trovato = pd.read_sql(query, connection)
        count -=1

        if count == 0:
            print("Operazione fallita")
            return None


    if count >0 :
        print("Ordine trovato")
        print(str(trovato.iloc[0]))
        query =f"DELETE FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
        connection.execute(text(query)) # serve per eseguire query che non devono restituire valori
        connection.commit()
        print("Ordine rimosso dal database")
    else :
        print("Errore")