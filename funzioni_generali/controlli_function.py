# funzione applicabile a tutte le classi
from datetime import date
#per il controllo di lunghezza stringa
#controllo del numero dei caratteri alfanumerici( va aggiunto se si riesce il controllo più specifico o messo come eccezione
def controlla(messaggio: str, lunghezza: int) -> str :
   parametro = input(messaggio)

   while len(parametro) != lunghezza :
        parametro = input(f" il parametro non è valido, riprovare : ")
   return parametro

#per il controllo delle date di scadenza
def check_date(data:str)->bool: #restituisce true quando può continuare , e false quando deve cessare le operazioni

    today = date.today() #funzione di Python che restituisce la data odierna
    data_odierna = today.strftime("%d/%m/%Y") #funzione di Python che applicata a today trasfroma il formato dato in stringa

    if int(data[6:10]) < int(data_odierna[6:10]): #controllo su anno
        print(f" data di scadenza passata ")
        return False
    elif int(data[6:10]) == int(data_odierna[6:10]):
        if int(data[3:5]) < int(data_odierna[3:5]) : #controllo mese
            print(f" data di scadenza passata ")
            return False
        elif int(data[3:5]) == int(data_odierna[3:5]):
            if int(data[0:2]) < int(data_odierna[0:2]): #controllo giorno
                print(f" data di scadenza passata ")
                return False
            elif int(data[0:2]) == int(data_odierna[0:2]):
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

def check_se_vuoto(messaggio: str) -> str :

   parametro = input(messaggio)

   while len(parametro) == 0 :
        parametro = input(f" il parametro non può essere vuoto, riprovare : ")
   return parametro
