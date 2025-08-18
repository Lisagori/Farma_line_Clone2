from funzioni_generali.controlli_function import check_date, check_se_vuoto, controlla, check_nascita
from classi.documenti.classe_tesserino_professionale import TesserinoProfessionale
from classi.documenti.classe_tessera_sanitaria import TesseraSanitaria
from funzioni_generali.random_function import create_random_string
from abc import ABC, abstractmethod
from datetime import datetime, date
from sqlalchemy import text
from db import connection
import pandas as pd
import random
import string


class Persona (ABC) :
    nome: str
    cognome: str

    def __init__(self):
        self.nome = check_se_vuoto("Inserire il proprio nome : ")
        self.cognome = check_se_vuoto("Inserire il proprio cognome : ")

    @abstractmethod
    def iscriversi(self) -> bool:
        ...

    @abstractmethod
    def crea_profilo(self) ->bool:
        ...

class ProfiloUtente(ABC):

    nome_utente: str
    password: str
    tipo_profilo: str
    id_utente :str

    def __init__(self, nome : str, password :str, id_u : str , tipo_p : str):
        self.nome_utente = nome
        self.password = password
        self.id_utente = id_u
        self.tipo_profilo = tipo_p

    @abstractmethod
    def associazione_profilo_utente(self) -> None:
        ...

    def controllo_nome_utente(self) -> bool:
        query = f"SELECT * FROM ProfiloUtente WHERE nome_utente = '{self.nome_utente}'"
        profilo_esistente = pd.read_sql(query, connection)
        if not profilo_esistente.empty:  # pd.read_sql(...) restituisce sempre un DataFrame di pandas.
            print(f"Il nome utente '{self.nome_utente}' è già in uso. Scegliere un altro nome.")
            return False
        else:
            return True


class ProfilolavoratoreSanitario(ProfiloUtente) :

    def associazione_profilo_utente(self) -> None:

        new_profile = pd.DataFrame(  # prf fa riferimento al profilo utente da associare alla relativa tebella
            columns=['nome_utente', 'password', 'tipo_profilo', 'id_sanitari'],
            data=[
                [self.nome_utente, self.password, self.tipo_profilo, self.id_utente]
            ]
        )
        new_profile.to_sql('ProfiloUtente', connection, if_exists='append', index=False)
        connection.commit()

        print("Profilo utente aggiunto con successo.")
        return None

class ProfiloCliente(ProfiloUtente) :
    __carrello: list[dict]   # si mette come attributo per evitare che il carrello si riazzeri ogni volta che viene chiamata da search_bar
    __quanto_compro: dict

    def __init__(self, nome : str, password :str, id_u : str , tipo_p : str):
        super().__init__(nome,password, id_u, tipo_p)
        self.__carrello= []
        self.__quanto_compro= {}

    def associazione_profilo_utente(self) -> None:

        new_profile = pd.DataFrame(  # prf fa riferimento al profilo utente da associare alla relativa tebella
            columns=['nome_utente', 'password', 'tipo_profilo', 'id_cliente'],
            data=[
                [self.nome_utente, self.password, self.tipo_profilo, self.id_utente]
            ]
        )
        new_profile.to_sql('ProfiloUtente', connection, if_exists='append', index=False)
        connection.commit()

        print("Profilo utente aggiunto con successo.")
        return None

    def search_bar(self) -> None:
        #richiama self.aggiunta_carrello
        medicinale: str
        filtri: str
        aggiungi_carrello: str

        print("BARRA DI RICERCA")
        filtri = input("Vuoi applicare dei filtri alla tua ricerca? (digitare si o no) : ")

        if filtri == "si":
            print("Indica almeno uno dei seguenti filtri, quando non si vuole mettere un filtro premere semplicemente invio")
            indicazioni_terapeutiche = input("Inserire le indicazioni terapeutiche : ")
            composizione = input("Inserire la composizione: ")
            posologia = input("Inserire la posologia : ")

            filters = []  # lista
            if indicazioni_terapeutiche:
                filters.append(f"LOWER(s.indicazioni_terapeutiche) LIKE LOWER ('%{indicazioni_terapeutiche}%')")

            if composizione:
                filters.append(f"LOWER (s.composizione) LIKE LOWER ('%{composizione}%')")

            if posologia:
                filters.append(f"LOWER (s.posologia) LIKE LOWER ('%{posologia}%')")

            query = """
                    SELECT 

                        f.codice AS codice_farmaco,      -- alias univoco
                        f.nome,
                        f.ricetta,
                        f.preparato_galenico,
                        f.prezzo,
                        f.quantità,
                        s.indicazioni_terapeutiche,
                        s.composizione,
                        s.eccipienti,
                        s.controindicazioni,
                        s.posologia,
                        s.avvertenze,
                        s.effetti_indesiderati
                    FROM FarmaciMagazzino AS f
                    JOIN SchedaTecnica AS s
                      ON f.codice = s.codice 
                    """
            if filters:
                query += " WHERE " + " AND ".join(filters)
                results = pd.read_sql(query, connection)

            else:
                print("Nessun filtro inserito. Ricerca annullata.")
                results = pd.DataFrame()  # equivalente a lista vuota

        elif filtri == "no":
            medicinale = input("Digitare il nome del farmaco che si sta cercando: ").strip()

            query = f"""
                    SELECT
                        f.codice AS codice_farmaco,      -- alias univoco
                        f.nome,
                        f.ricetta,
                        f.preparato_galenico,
                        f.prezzo,
                        f.quantità,
                        s.indicazioni_terapeutiche,
                        s.composizione,
                        s.eccipienti,
                        s.controindicazioni,
                        s.posologia,
                        s.avvertenze,
                        s.effetti_indesiderati
                    FROM FarmaciMagazzino AS f
                    JOIN SchedaTecnica AS s
                      ON f.codice = s.codice
                        WHERE LOWER(TRIM(f.nome)) LIKE LOWER('%{medicinale}%') -- TRIM dà più tolleranza sugli spazi
                                """
            results = pd.read_sql(query, connection)
        else:
            print("Operazione non valida.")
            results = pd.DataFrame()  # equivalente a lista vuota

        # Stampa dei risultati
        if not results.empty:
            for farmaco in results.to_dict(orient="records"):
                print(farmaco)
            self.aggiunta_carrello(results)

        if results.empty:
            print("Nessun farmaco trovato.")
            return  # torna al menu precedente

    def aggiunta_carrello(self,results) -> None:

        ck: bool = False
        ck_se_presente : bool = False
        controllo_q: bool = False
        verifica_cod: bool = False
        quantity: int = 0
        codice_input: str = ''

        # sezione dedicata al controllo del codice se è presente o meno nell'elenco trovato nella ricerca
        # Se ce più di un farmaco
        if len(results) > 1:
            while not ck:
                codice_input = input("\nInserire il codice del farmaco che si vuole acquistare: ")

                for prodotto in results.to_dict(orient="records"):
                    if codice_input == prodotto["codice_farmaco"]:
                        verifica_cod = True
                        break
                    else:
                        verifica_cod = False

                if not verifica_cod:
                    print("Il codice inserito non è valido, o non è presente tra quelli elencati")
                else:
                    ck = True
        # Se ce n'è solo uno
        else:
            codice_input = (results.iloc[0]["codice_farmaco"])

        #ricerca se il prodotto era già stato aggiunto al carrello
        for contenuto in self.__carrello :
            if codice_input == contenuto["codice_farmaco"]:
                ck_se_presente = True
                break

        # sezione di codice per controllare che la quantità che si vuole acquistare sia disponibile
        while not controllo_q: #  consente di riprovare se non è sufficente la quantità
            ck = False
            while not ck:
                try:
                    quantity = int(input("Inserire la quantità di prodotto che si vuole aqcuistare : "))
                    ck = True
                except ValueError:
                    ck = False
                    print("il valore inserito non è compatibile, riprovare")


            if ck_se_presente :
                print(self.__quanto_compro)
                quantity = quantity + self.__quanto_compro[codice_input]

            query = f"SELECT quantità FROM FarmaciMagazzino WHERE quantità < '{quantity}' AND codice = '{codice_input}' "
            q_trovato = pd.read_sql(query, connection)

            if q_trovato.empty:
                aggiungi_carrello = input("\nDigitare 'si' se si vuole aggiungere il prodotto al carrello, altrimenti digitare 'no': ")

                if aggiungi_carrello == "si":

                    # recupera la riga che contiene le informazioni del farmaco che si vuole acquistare
                    riga = results.loc[results["codice_farmaco"] == codice_input]
                    farmaco_dict = riga.iloc[0].to_dict()# prende la prima corrispondenza

                    if not ck_se_presente : # aggiunge al  carrelo solo se non ho messo nel carrello lo stesso prodotto
                        self.__carrello.append(farmaco_dict)
                        self.__quanto_compro[codice_input]= quantity
                    else :
                        self.__quanto_compro[codice_input] = quantity

                    print("Farmaco aggiunto al carrello.")

                    # stampa del carrello
                    print("Contenuto attuale del carrello:")
                    if self.__carrello:
                        for prodotto in self.__carrello:
                            print(f" codice : {prodotto["codice_farmaco"]} ")
                            print(f" nome : {prodotto["nome"]} ")
                            print(f" quantità : {self.__quanto_compro[prodotto["codice_farmaco"]]} ")
                            print(f" prezzo : {self.__quanto_compro[prodotto["codice_farmaco"]] * float(prodotto["prezzo"])}")

                    else:
                        print("Il carrello è vuoto.")

                elif aggiungi_carrello == "no":
                    print("Farmaco non aggiunto al carrello")
                    print("Contenuto attuale del carrello:")

                    #stampa del carrello
                    if self.__carrello:

                        for prodotto in self.__carrello:
                            print(f" codice : {prodotto["codice_farmaco"]} ")
                            print(f" nome : {prodotto["nome"]} ")
                            print(f" quantità : {self.__quanto_compro[prodotto["codice_farmaco"]]} ")
                            print(f" prezzo : {self.__quanto_compro[prodotto["codice_farmaco"]] * float(prodotto["prezzo"])}")

                    else:
                        print("Il carrello è vuoto.")
                else:
                    print("Operazione non valida.")

                controllo_q = True
            else: # non trova riscontri in magazzino
                if q_trovato.iloc[0, 0] == 0:
                    print("Il prodotto è terminato non è possibile acquistarlo")
                    controllo_q = True
                else:
                    print("La quantità di farmaco in magazzino non è sufficiente, riprovare  ")

    def scelta_indirizzi(self) -> None:

        indirizzo_domicilio: str
        scelta_ind: str = "exit"
        controllo_ricetta: int
        ck_pagamento :bool

        controllo_ricetta = self.verifica_dati_ricetta()

        if len(self.__carrello) > 0 :
            if controllo_ricetta == 0:
                print("per ricevere l'ordine a domicilio digitare 1")
                print("per ritirare l'ordine nella farmacia fisica 2")
                scelta_ind = input()
            elif controllo_ricetta > 0:
                scelta_ind= "2"

            if scelta_ind == "1":
                indirizzo_domicilio = input("Inserire l'indirizzo di domicilio a cui si vuole ricevere l'ordine : ")
                print(f"Operazione andata a buon fine, l'ordine sarà spedito presso {indirizzo_domicilio}")
                ck_pagamento = self.pagare(indirizzo_domicilio)
                if not ck_pagamento:
                    print("Operazione terminata")

            elif scelta_ind== "2":
                print("L'ordine potrà essere ritirato entro 10 giorni presso la nostra sede fisica in Via Univeristà di Santa Marta, 26")
                print("Operazione andata a buon fine")

                ck_pagamento = self.pagare("Via Univeristà di Santa Marta, 26")

                if not ck_pagamento:
                    print("Operazione terminata")

            else:
                print("operazione non valida ")
        else :
            print("il carrello è vuoto , l'operazione di acquisto verrà terminata")

    def verifica_dati_ricetta(self) -> int:

        count: int = 0
        nome_farma : str

        for prodotto in self.__carrello:
            #si ricerca tra i prodotti nel carrello quelli che necessitano di ricetta
            codice_val = prodotto["codice_farmaco"]
            nome_farma = prodotto["nome"]
            query = f" SELECT ricetta FROM FarmaciMagazzino WHERE codice = '{codice_val}' AND ricetta = 'si'"
            serve_ricetta = pd.read_sql_query(query, connection)  # può restituire si o rimanere vuoto

            if not serve_ricetta.empty:

                # controllo se l'utente è in possesso della ricetta per acquistare il farmaco
                query = f" SELECT codice_farmaco FROM Ricetta WHERE codice_farmaco ='{codice_val}' AND codice_fiscale = '{self.id_utente}'"
                nome_ck = pd.read_sql_query(query, connection)

                if nome_ck.empty:

                    print(f"Non è associata nessuna ricetta per {nome_farma} al profilo corrente, il prodotto con ricetta verrà eliminato dal carrello")
                    self.__carrello.remove(prodotto)
                    del self.__quanto_compro[prodotto["codice_farmaco"]]

                if not nome_ck.empty:
                    count += 1

        return count

    def pagare(self, indirizzo: str) -> bool:

        ck_data: bool
        ck_opzioni : bool = False
        metodo: str
        prezzo_tot: float = 0

        for prodotto in self.__carrello:
            print(f" codice : {prodotto["codice_farmaco"]} ")
            print(f" nome : {prodotto["nome"]} ")
            print(f" quantità : {self.__quanto_compro[prodotto["codice_farmaco"]]} ")
            print(f" prezzo : {self.__quanto_compro[prodotto["codice_farmaco"]] * float(prodotto["prezzo"])}")

        print(self.__quanto_compro)

        for prodotto in self.__carrello:
            prezzo_tot = prezzo_tot + float(prodotto["prezzo"]) * self.__quanto_compro[prodotto["codice_farmaco"]]

        print(f"Prezzo totale dell'ordine : {prezzo_tot} €")

        while not ck_opzioni :
            print("se si desidera procedere all'acquisto digitare 1")
            print("se si desidera annullare l'operazione digitare exit")
            scelta = input()

            while scelta == "1":
                print("Scegliere metodo di pagamento")
                print("digitare 1 per pagare con carta di credito o debito (American Express, Euro/Mastercard, Visa, Maestro)")
                print("digitare 2 per pagare con portafoglio digitale (paypal , Google pay, Apple pay)")
                metodo = input()

                if metodo == "1":

                    print("INSERIMENTO DATI CARTA")
                    nome = input("Inserire il nome dell'intestatario : ")
                    cognome = input("Inserire il cognome dell'intestatario : ")
                    numero_carta = controlla("Inserire numero della carta : ", 16)
                    data_input = controlla("Inserire  data di scadenza della carta(gg/mm/aaaa): ", 10)
                    ck_data= False
                    while not ck_data:
                        try:
                            data_scadenza = datetime.strptime(data_input, "%d/%m/%Y").date()
                            ck_data = True
                        except ValueError:
                            print("Data non valida!")
                            ck_data= False
                    cvc = controlla("Inserire il CVC : ", 3)

                    print("DATI DELLA CARTA")
                    print(f"NOME : {nome}")
                    print(f"COGNOME : {cognome}")
                    print(f"NUMERO CARTA : {numero_carta}")
                    print(f"DATA SCADENZA : {data_scadenza}")
                    print(f"CVC : {cvc}")

                    ck_data = check_date(data_scadenza)
                    if not ck_data:
                        print("operazione fallita")#carta scaduta
                        return False
                    else:
                        print("operazione andata a buon fine")
                        self.associa_numero_ordine(indirizzo)

                        for prodotto in self.__carrello:
                            #si modifica la quantità di prodotto in magazzino
                            new_quantity = prodotto["quantità"] - self.__quanto_compro[prodotto["codice_farmaco"]]
                            query = f"UPDATE FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{prodotto["codice_farmaco"]}' "
                            connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                            connection.commit()
                            # si elimina la ricetta utilizzata nell'acquisto
                            query = f"DELETE FROM Ricetta WHERE codice_farmaco ='{prodotto["codice_farmaco"]}' AND codice_fiscale = '{self.id_utente}' "
                            connection.execute(text(query))
                            connection.commit()

                        return True

                elif metodo == "2":
                    print("operazione andata a buon fine")
                    self.associa_numero_ordine(indirizzo)

                    for prodotto in self.__carrello:
                        # si modifica la quantità di prodotto in magazzino
                        new_quantity = prodotto["quantità"] - self.__quanto_compro[prodotto["codice_farmaco"]]
                        query = f"UPDATE FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{prodotto["codice_farmaco"]}' "
                        connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                        connection.commit()
                        # si elimina la ricetta utilizzata nell'acquisto
                        query = f"DELETE FROM Ricetta WHERE codice_farmaco ='{prodotto["codice_farmaco"]}' AND codice_fiscale = '{self.id_utente}' "
                        connection.execute(text(query))
                        connection.commit()

                    return True

                else :
                    print("Opzione non valida, riprovare")

            if scelta == "exit":
                return False
            else:
                print("Opzione non valida, riprovare")

    def associa_numero_ordine( self, indirizzo: str) -> None:

        num_ordine: int

        num_ordine = random.randint(0, 1000000000)
        print(f"Fornire il seguente codice al momento del ritiro : {num_ordine}")

        new_ordine = pd.DataFrame(
            [[
                num_ordine,
                self.id_utente,
                indirizzo,
            ]],
            columns=[
                'numero_ordine',  # <-- niente spazio finale
                'cf',
                'indirizzo',
            ]
        )
        new_ordine.to_sql('Ordine', connection, if_exists='append', index=False)
        connection.commit()

class ProfiloFarmacista(ProfilolavoratoreSanitario) :

    @staticmethod
    def verifica_ordine() -> None:

        cod_fisc: str
        n_ordine: str
        count: int = 3

        print("RICERCA ORDINE NEL DATABASE")

        cod_fisc = check_se_vuoto("Inserire il codice fiscale del cliente : ")
        n_ordine = check_se_vuoto("Inserire il numero dell'ordine : ")

        query = f"SELECT * FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
        trovato = pd.read_sql(query, connection)

        while trovato.empty:

            print(f"Ordine non trovato, riprovare (tentativi rimasti {count}")
            cod_fisc = check_se_vuoto("Inserire il codice fiscale del cliente : ")
            n_ordine = check_se_vuoto("Inserire il numero dell'ordine : ")

            query = f"SELECT * FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
            trovato = pd.read_sql(query, connection)
            count -= 1

            if count == 0:
                print("Operazione fallita")
                return None

        if count > 0:
            print("Ordine trovato")
            print(str(trovato.iloc[0]))
            query = f"DELETE FROM Ordine WHERE numero_ordine = '{n_ordine}' AND cf = '{cod_fisc}' AND indirizzo = 'Via Univeristà di Santa Marta, 26' "
            connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
            connection.commit()
            print("Ordine rimosso dal database")
        else:
            print("Errore")

    @staticmethod
    def aggiorna_magazzino() -> None:

        scelta_op: str
        controllo_scelta: bool = False
        continua: str = "1"
        new_quantity: int = 0

        query = "SELECT codice, nome, quantità FROM FarmaciMagazzino WHERE quantità <= 2 "
        riordinare = pd.read_sql(query, connection)

        if not riordinare.empty:
            print("ATTENZIONE!! I seguenti farmaci stanno per terminare o sono già terminati ")
            for farmaco in riordinare.to_dict(orient="records"):
                print(farmaco)
        else:
            return None

        while not controllo_scelta:
            print("Se si vuole aggiornare le quantità dei farmaci sopra elencati digitare 1")
            print("Per procedere con altre operazioni digitare 2")
            scelta_op = input()

            if scelta_op == "1":

                controllo_scelta = True

                while continua == "1":
                while verifica == "1":
                    new_quantity=0
                    cod = input("Inserire il codice del farmaco che si vuole aggiornare : ")

                    query = f"SELECT codice FROM FarmaciMagazzino WHERE codice = '{cod}' AND quantità <= 2 "
                    ricerca = pd.read_sql(query, connection)

                    if not ricerca.empty:
                        while new_quantity <= 0:
                            try:
                                new_quantity = int(input("Inserire la quantità aggiornata : "))
                            except ValueError:
                                print("Il valore inserito non è compatibile, riprovare ")

                            if new_quantity <= 0:
                                print("Il parametro non può assumere valore negativo o nullo")

                        query = f"UPDATE FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{cod}'"
                        connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                        connection.commit()

                        query = "SELECT codice, nome, quantità FROM FarmaciMagazzino WHERE quantità <= 2 "
                        new_elenco = pd.read_sql(query, connection)

                        if not new_elenco.empty:
                            print("ELENCO AGGIORNATO")
                            for farmaco in new_elenco.to_dict(orient="records"):
                                print(farmaco)
                        else:
                            return None

                        print("Se si desidera continuare ad aggiornare le quantità digitare 1 ")
                        print("Per procedere con altre operazioni digitare 2 ")
                        verifica = input()
                        if verifica!= '2':
                            print("operazione non valida, riprovare")
                        continua = input()

                    else:
                        print("Il codice inserito non è presente nella lista fornita , riprovare ")
                        continua = "1"

            elif scelta_op == "2":
                return None

            else:
                print("Operazione non valida")
                controllo_scelta = False

    @staticmethod
    def aggiunta_farmaci() -> None:

        ck: bool = False
        nome: str
        ricetta: str
        preparato_galenico: str
        quanto: int = 0
        prezzo: float = 0.0

        print("Per aggiungere una nuova tipologia di medicinale in magazzino, seguire le istruzioni di seguito riportate ")

        query = "SELECT MAX(codice) FROM FarmaciMagazzino"
        cod = pd.read_sql(query, connection)
        cod = str(cod.iloc[0, 0])

        if cod == "None":#caso di databse vuoto
            cod = "1"
        else :
            cod = str(int(cod) + 1)

        nome = check_se_vuoto("Inserire il nome del farmaco : ")
        ricetta = check_se_vuoto("Il farmaco necessita di ricetta ? (digitare si o no) : ")
        preparato_galenico = check_se_vuoto("È un preparato galenico ? (digitare si o no) : ")

        while quanto <= 0:
            try:
                quanto = int(input("Inserire la quantità di farmaco che si vuole aggiungere in magazzino : "))
            except ValueError:
                print("Il valore inserito non è compatibile, riprovare")
            if quanto <= 0:
                print("Il parametro non può assumere valore negativo o nullo")

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
        posologia = check_se_vuoto("Inserire la posologia : ")
        avvertenze = check_se_vuoto("Inserire le avvertenze : ")
        effetti_indesiderati = check_se_vuoto("Inserire gli effetti indesiderati : ")


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

class ProfiloMedico(ProfilolavoratoreSanitario) :

    def crea_ricetta(self) -> None: #funzione medico

        ck_cod: bool= False
        cod: str
        i: int

        print("Digitare il codice del farmaco che si vuole prescrivere, selezionando dal segunete elenco ")

        query = "SELECT codice , nome FROM FarmaciMagazzino WHERE ricetta = 'si' "
        elenco = pd.read_sql(query, connection)

        if not elenco.empty:
            for farmaco in elenco.to_dict(orient="records"):
                print(farmaco)

            while not ck_cod:

                cod_farmaco = input()
                query = f"SELECT nome FROM FarmaciMagazzino WHERE codice='{cod_farmaco}' AND ricetta = 'si'"
                farma = pd.read_sql(query, connection)

                if not farma.empty:
                    cod_fisc = controlla("Inserire il codice fiscale del paziente a cui si sta prescrivendo il farmaco : ", 16)

                    cod_ricetta = ((create_random_string(4, string.digits)
                                   + create_random_string(1, string.ascii_uppercase))
                                   + ' '
                                   + create_random_string(10, string.digits))

                    new_ricetta = pd.DataFrame(
                        [[
                            cod_ricetta,
                            cod_fisc,
                            cod_farmaco,
                            self.nome_utente
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

                    print(f"Fornire il seguente codice al paziente , CODICE RICETTA : {cod_ricetta}")
                    ck_cod=True

                else:
                    print("Il codice inserito non appartiente a nessun farmaco nell'elenco , riprovare: ")
                    ck_cod=False

        else:
            print("Non ci sono farmaci con ricetta da poter prescrivere in magazzino")


class LavoratoreSanitario (Persona) :#classe base

    t_p: TesserinoProfessionale  # t_p abbreviazione tesserino professionale

    def iscriversi(self) -> bool:

        ck_scelta: bool = False
        query = f"SELECT * FROM Sanitari WHERE matricola = '{self.t_p.n_matricola}'"
        lav_sani = pd.read_sql(query, connection)

        # si definisce la ricerca da database per controllare se la persona è già registrata
        if not lav_sani.empty:  # è un dataframe
            print("La matricola inserita appartiene a un utente già registrato")

            while not ck_scelta:
                print("Se si vuole accedere al servizio digitare 1")
                print("Se si vuole ritentare il processo di iscrizione digitare 2")
                print("Digitare exit se si vuole terminare l'operazione")
                scelta = check_se_vuoto("")

                if scelta == "1":
                    return True
                elif scelta == "2":
                    self.t_p.n_matricola = input("Inserire il numero di matricola corretto : ")
                    return self.iscriversi()
                elif scelta== "exit":
                    return False
                else:
                    print("operazione non valida,riprovare ")
                    ck_scelta= False

        else:
            self.t_p.associazione_tessera_a_db()
            new_lav_sani = pd.DataFrame(
                columns=['nome', 'cognome', 'professione', 'matricola'],
                data=[
                    [self.nome, self.cognome, self.t_p.ordine_di_appartenenza, self.t_p.n_matricola]
                ]
            )
            new_lav_sani.to_sql('Sanitari', connection, if_exists='append', index=False)
            connection.commit()

            # sezione per associazione profilo utente
            return self.crea_profilo()

    def crea_profilo(self) ->bool:

        print("CREAZIONE PROFILO UTENTE")
        nome = check_se_vuoto(" inserire un nome utente : ")  # inserire controllo per corrispondenza profilo utente
        password = check_se_vuoto(" inserire una password : ")

        profilo = ProfilolavoratoreSanitario(nome, password, self.t_p.n_matricola, self.t_p.ordine_di_appartenenza)

        ck = profilo.controllo_nome_utente()

        while not ck:  # questo nuovo
            nuovo_nome = check_se_vuoto("Inserisci un altro nome utente: ")
            profilo.nome_utente = nuovo_nome
            ck = profilo.controllo_nome_utente()

        profilo.associazione_profilo_utente()

        print("registrazione effettuata con successo.")
        print(f"        Benvenuto {profilo.nome_utente} !")
        return True

class Cliente(Persona):
    t_s: TesseraSanitaria #t_s abbreviazione tessera sanitaria

    def __init__(self):
        super().__init__()
        self.t_s = TesseraSanitaria()

    def iscriversi(self, ty_p :str ='') -> bool:

        ck_data: bool

        self.t_s.data_nascita = check_nascita(self.t_s.data_nascita)# per verificare che la data di nascita non indichi una data futura
        ck_data= check_date(self.t_s.data_scadenza)# per verificare che la tessera registrata non sia scaduta


        if ck_data and self.t_s.data_nascita != date.today()  :
            #per verificare che il codice inserito non appartenga a un'altra tessera sanitaria
            query = f"SELECT * FROM Clienti WHERE codice_fiscale = '{self.t_s.codice_fiscale}'"
            cliente = pd.read_sql(query, connection)
            if not cliente.empty: # è un dataframe
                print("Il codice fiscale inserito appartiene a un utente già registrato")
                print("Se si vuole accedere al servizio digitare 1")
                print("Se si vuole ritentare il processo di iscrizione digitare 2")
                print("Digitare exit se si vuole terminare l'operazione")
                scelta = input()

                if scelta == "1":
                    return True
                elif scelta == "2":
                    self.t_s.codice_fiscale = input("Inserire il codice fiscale corretto : ")
                    return self.iscriversi()
                else:
                    return False

            else:
                self.t_s.associazione_tessera_a_db()
                new_cliente = pd.DataFrame(
                    columns=['nome','cognome','codice_fiscale'],
                    data=[
                    [self.nome, self.cognome, self.t_s.codice_fiscale ]
                    ]
                )
                new_cliente.to_sql('Clienti', connection, if_exists='append', index=False)
                connection.commit()
                #sezione per associazione profilo utente
                return self.crea_profilo()
        else:
            print("La tessera risulta scaduta o la data di nascita non è valida, non è possibile effettuare l'iscrizione al servizio")
            return False

    def crea_profilo(self) ->bool:

        print("CREAZIONE PROFILO UTENTE")
        nome = check_se_vuoto(" inserire un nome utente : ")  # inserire controllo per corrispondenza profilo utente
        password = check_se_vuoto(" inserire una password : ")
        profilo = ProfiloCliente(nome, password, self.t_s.codice_fiscale, 'cliente')
        ck = profilo.controllo_nome_utente()

        while not ck:  # questo nuovo
            nuovo_nome = check_se_vuoto("Inserisci un altro nome utente: ")
            profilo.nome_utente = nuovo_nome
            ck = profilo.controllo_nome_utente()

        profilo.associazione_profilo_utente()

        print("registrazione effettuata con successo.")
        print(f"        Benvenuto {profilo.nome_utente} !")
        return True

class Farmacista(LavoratoreSanitario):

    def __init__(self):
        super().__init__()
        self.t_p = TesserinoProfessionale("farmacista")

class Medico(LavoratoreSanitario):

    def __init__(self):
        super().__init__()
        self.t_p = TesserinoProfessionale("medico")
