import pandas as pd
from sqlalchemy import text

from db import connection, engine


def verifica_ordine()-> None :

    cod_fisc:str
    n_ordine :str
    count : int = 3

    cod_fisc = input("Inserire il codice fiscale del cliente : ")
    n_ordine = input("Inserire il numero dell'ordine : ")

    query = f"SELECT * FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
    trovato = pd.read_sql(query, connection)

    while trovato.empty :

        print(f"Ordine non trovato, riprovare (tentativi rimasti {count}")
        cod_fisc = input("Inserire il codice fiscale del cliente : ")
        n_ordine = input("Inserire il numero dell'ordine : ")

        query = f"SELECT * FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
        trovato = pd.read_sql(query, connection)
        count -=1

    if count == 0 :
        print("Operazione fallita")
    elif count >0 :
        print("Ordine trovato")
        print(str(trovato.iloc[0]))
        query =f"DELETE FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
        connection.execute(text(query)) # serve per eseguire query che non devono restituire valori
        connection.commit()
        print("Ordine rimosso dal database")