# funzione applicabile a tutte le classi
from datetime import date
#per il controllo di lunghezza stringa
def controlla(messaggio: str, lunghezza: int) -> str : #controllo del numero dei caratteri alfanumerici( va aggiunto se si riesce il controllo più specifico o messo come eccezione
   parametro = input(messaggio)

   while len(parametro) != lunghezza :
        parametro = input(f" il parametro non è valido, riprovare : ")
   return parametro

#per il controllo delle date di scadenza
def check_date(data:str)->bool: #restituisce true quando può continuare , e false quando deve cessare le operazioni
    today :str
    data_odierna :str

    today = date.today()
    data_odierna = today.strftime("%d/%m/%Y")

    if int(data[7:]) < int(data_odierna[7:]):
        print(f" data di scadenza passata ")
        return False
    elif int(data[7:]) == int(data_odierna[7:]):
        if int(data[4:6]) < int(data_odierna[4:6]) :
            print(f" data di scadenza passata ")
            return False
        elif int(data[4:6]) == int(data_odierna[4:6]):
            if int(data[1:3]) < int(data_odierna[1:3]):
                print(f" data di scadenza passata ")
                return False
            elif int(data[1:3]) == int(data_odierna[1:3]):
                verifica = input("la scadenza è oggi, sei sicuro di voler proseguire?(digita si o no)")
                if verifica == "si":
                    return True
                elif verifica == "no" :
                    return False
            else :
                return True
        else:
            return True
    else:
        return True