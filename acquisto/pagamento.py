from sqlalchemy import text
from acquisto.creazione_ordine import associa_numero_ordine
from db import connection
from funzioni_generali.controlla import controlla, check_date
from acquisto.carrello import carrello, quanto_compro

#operazioni superficiali per concludere il caso d'uso , non viene fatto un collegamento con la banca
def pagare(indirizzo :str) ->bool:

    ck : bool
    metodo:str
    prezzo_tot : float = 0
    i : int = 0

    print(carrello)
    for prodotto in carrello :
        prezzo_tot = prezzo_tot + float(prodotto["prezzo"]) * quanto_compro[i]
        i +=1

    print(f"Prezzo totale dell'ordine : {prezzo_tot} €")

    print("se si desidera procedere all'acquisto digitare 1")
    print("se si desidera annullare l'operazione digitare exit")
    scelta = input()

    if scelta =="1":
        print("Scegliere metodo di pagamento")
        print("digitare 1 per pagare con carta di credito o debito (American Express, Euro/Mastercard, Visa, Maestro)")
        print("digitare 2 per pagare con portafoglio digitale (paypal , Google pay, Apple pay)")
        metodo = input()

        if metodo =="1":

            print("INSERIMENTO DATI CARTA")
            nome = input("Inserire il nome dell'intestatario : ")
            cognome = input("Inserire il cognome dell'intestatario : ")
            numero_carta = controlla("Inserire numero della carta : ", 16)
            data_scadenza = controlla("Inserire  data di scadenza della carta(gg/mm/aaaa): ", 10)
            cvc = controlla("Inserire il CVC : ", 3)

            ck = check_date(data_scadenza)
            if not ck :
                print("operazione fallita")
                return False
            else :
                print("operazione andata a buon fine")
                associa_numero_ordine(indirizzo)
                i = 0
                for prodotto in carrello :
                    new_quantity = prodotto["quantità"] - quanto_compro[i]
                    query = f"UPDATE INTO FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{prodotto["codice_farmaco"]}' "
                    connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                    connection.commit()
                    i += 1

                return True

        elif metodo =="2":
            print("operazione andata a buon fine")
            associa_numero_ordine(indirizzo)
            for prodotto in carrello:
                new_quantity = prodotto["quantità"] - quanto_compro[i]
                query = f"UPDATE FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{prodotto["codice_farmaco"]}' "
                connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                connection.commit()
                i += 1
            return True
    elif scelta == "exit":
        return False