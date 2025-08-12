from funzioni_generali.controlla import controlla, check_date


#operazioni superficiali per concludere il caso d'uso , non viene fatto un collegamento con la banca
def pagare() ->None:

    ck : bool
    metodo:str

    print("Scegliere metodo di pagamento")
    print("digitare 1 per pagare con carta di credito o debito (American Express, Euro/Mastercard, Visa, Maestro)")
    print("digitare 2 per pagare con portafoglio digitale (paypal , Google pay, Apple pay)")
    metodo = input()

    if metodo =="1":

        print("INSERIMENTO DATI CARTA")
        nome = input("Inserire il nome dell'intestatario : ")
        cognome = input("Inserire il cognome dell'intestatario : ")
        numero_carta = controlla("Inserire numero della carta : ", 16)
        data_scadenza = controlla("Inserire  data di scadenza della carta(gg/mm/aaaa): ", 10)#todo controllo data scendza se scaduta
        cvc = controlla("Inserire il CVC : ", 3)

        ck = check_date(data_scadenza)
        if not ck :
            print("operazione fallita")
        else :
            print("operazione andata a buon fine")

    elif metodo =="2":
        print("operazione andata a buon fine")