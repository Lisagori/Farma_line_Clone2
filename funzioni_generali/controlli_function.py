# funzione applicabile a tutte le classi
from datetime import date
from datetime import datetime
#per il controllo di lunghezza stringa
#controllo del numero dei caratteri alfanumerici( va aggiunto se si riesce il controllo più specifico o messo come eccezione
def controlla(messaggio: str, lunghezza: int) -> str :
   parametro = input(messaggio)

   while len(parametro) != lunghezza :
        parametro = input(f" il parametro non è valido, riprovare : ")
   return parametro

#per il controllo delle date di scadenza
def check_nascita(data:datetime.date)-> date: #restituisce true quando può continuare , e false quando deve cessare le operazioni
    ck: bool
    today = date.today() #funzione di Python che restituisce la data odierna
    for i in reversed ( range (3)):
        try:
            data = input("Inserire la data di nascita corretta : ")
            data = datetime.strptime(data, "%d/%m/%Y").date()
            if data > today: #controllo su anno
                print(f"data di nascita non valida, riprovare (rimangono {i})")
            else:
                return data
        except ValueError:
            print("formato della data non valida , riprovare")

    return today

def check_date(
        data: datetime.date) -> bool:  # restituisce true quando può continuare , e false quando deve cessare le operazioni

    today = date.today()  # funzione di Python che restituisce la data odierna

    if data < today:  # controllo su anno
        print(" data di scadenza passata ")
        return False
    elif data == today:
        print("La scadenza è oggi, sei sicuro di voler proseguire? Digita si o no")
        verifica = input()
        if verifica == "si":
            return True
        elif verifica == "no":
            return False
    else:
        return True

def check_se_vuoto(messaggio: str) -> str :

   parametro = input(messaggio)

   while len(parametro) == 0 :
        parametro = input(f" il parametro non può essere vuoto, riprovare : ")
   return parametro
