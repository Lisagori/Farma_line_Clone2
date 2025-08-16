import random
import string
from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy import text
from db import connection
from classi.documenti.classe_tessera_sanitaria import TesseraSanitaria
from classi.documenti.classe_tesserino_professionale import TesserinoProfessionale
from funzioni_generali.random_function import create_random_string
from funzioni_generali.controlli_function import check_date, check_se_vuoto, controlla

carrello: list[dict] = [] #si inserisce fuori dalla funzione per evitare che il carrello si riazzeri ogni volta che viene chiamata da search_bar
quanto_compro : list[int] = []

class Persona (ABC) :
    nome: str
    cognome: str

    def __init__(self):
        self.nome = input("Inserire il proprio nome : ")
        self.cognome = input("Inserire il proprio cognome : ")

    @abstractmethod
    def iscriversi(self) -> bool:
        ...

    @abstractmethod
    def crea_profilo(self) ->bool:
        ...

class ProfiloUtente(ABC):
    id_utente :str
    nome_utente: str
    password: str
    tipo_profilo :str

    def __init__(self, nome : str, password :str, id_u : str , tipo_p : str):
        self.nome_utente = nome
        self.password = password
        self.id_utente = id_u
        self.tipo_profilo = tipo_p

    @abstractmethod
    def associazione_profilo_utente(self) -> None:
        ...

    def controllo_utente(self) -> bool:
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

    @staticmethod
    def aggiunta_carrello(results) -> None:

        ck: bool = False
        controllo: bool = False
        verifica: bool = False
        quantity: int = 0
        codice_input: str = ''

        i: int

        # sezione dedicata al controllo del codice se è presente o meno nell'elenco trovato nella ricerca
        if len(results) > 1:  # Se ce più di un farmaco
            while not ck:
                codice_input = input("\nInserire il codice del farmaco che si vuole acquistare: ")

                for prodotto in results.to_dict(orient="records"):
                    if codice_input == prodotto["codice_farmaco"]:
                        verifica = True
                        break
                    else:
                        verifica = False

                if not verifica:
                    print("Il codice inserito non è valido")
                else:
                    ck = True
        else:  # Se ce n'è solo uno
            codice_input = (results.iloc[0]["codice_farmaco"])

        # sezione di codice per controllare che la quantità che si vuole acquistare sia disponibile

        while not controllo:
            ck = False
            while not ck:
                try:
                    quantity = int(input("Inserire la quantità di prodotto che si vuole aqcuistare : "))
                    ck = True
                except ValueError:
                    print("il valore inserito non è compatibile, riprovare")

            query = f"SELECT quantità FROM FarmaciMagazzino WHERE quantità < '{quantity}' AND codice = '{codice_input}' "
            q_trovato = pd.read_sql(query, connection)

            if q_trovato.empty:
                aggiungi_carrello = input("\nDigitare 'si' se si vuole aggiungere il prodotto al carrello, altrimenti digitare 'no': ")
                quanto_compro.append(quantity)

                if aggiungi_carrello == "si":
                    # results: DataFrame con almeno la colonna "codice"

                    riga = results.loc[results["codice_farmaco"] == codice_input]

                    if not riga.empty:
                        farmaco_dict = riga.iloc[0].to_dict()  # prendo la prima corrispondenza
                        carrello.append(farmaco_dict)
                        print("Farmaco aggiunto al carrello.")
                    else:
                        print("Codice non trovato tra i risultati mostrati.")

                    print("Contenuto attuale del carrello:")

                    if carrello:
                        i = 0
                        for prodotto in carrello:
                            print(f" codice : {prodotto["codice_farmaco"]} ")
                            print(f" nome : {prodotto["nome"]} ")
                            print(f" quantità : {quanto_compro[i]} ")
                            print(f" prezzo : {quanto_compro[i] * float(prodotto["prezzo"])}")
                            i += 1
                    else:
                        print("Il carrello è vuoto.")

                elif aggiungi_carrello == "no":
                    print("Farmaco non aggiunto al carrello")
                    print("Contenuto attuale del carrello:")

                    if carrello:
                        i = 0
                        for prodotto in carrello:
                            print(f" codice : {prodotto["codice_farmaco"]} ")
                            print(f" nome : {prodotto["nome"]} ")
                            print(f" quantità : {quanto_compro[i]} ")
                            print(f" prezzo : {quanto_compro[i] * float(prodotto["prezzo"])}")
                            i += 1

                        #print(pd.DataFrame(carrello).to_string(index=False))
                    else:
                        print("Il carrello è vuoto.")
                else:
                    print("Operazione non valida.")

                controllo = True
            else:
                if q_trovato.iloc[0, 0] == 0:
                    print("Il prodotto è terminato non è possibile acquistarlo")
                    controllo = True
                else:
                    print("La quantità di farmaco in magazzino non è sufficiente, riprovare  ")

    def scelta_indirizzi(self) -> None:

        indirizzo_domicilio: str
        scelta: str = "exit"
        controllo: int

        controllo = self.inserimento_dati_ricetta()

        if len(carrello) > 0 :
            if controllo == 0:
                print("per ricevere l'ordine a domicilio digitare 1")
                print("per ritirare l'ordine nella farmacia fisica 2")
                scelta = input()
            elif controllo > 0:
                scelta = "2"

            if scelta == "1":
                indirizzo_domicilio = input("Inserire l'indirizzo di domicilio a cui si vuole ricevere l'ordine : ")
                print(f"Operazione andata a buon fine, l'ordine sarà spedito presso {indirizzo_domicilio}")
                controllo = self.pagare(indirizzo_domicilio)
                if not controllo:
                    print("Operazione terminata")

            elif scelta == "2":
                print(
                    "L'ordine potrà essere ritirato entro 10 giorni presso la nostra sede fisica in Via Univeristà di Santa Marta, 26")
                print("Operazione andata a buon fine")

                controllo = self.pagare("Via Univeristà di Santa Marta, 26")

                if not controllo:
                    print("Operazione terminata")

            else:
                print("operazione non valida ")
        else :
            print("il carrello è vuoto , l'operazione di acquisto verrà terminata")

    def inserimento_dati_ricetta(self) -> int:

        count: int = 0
        i: int = 0

        for prodotto in carrello:
            #si ricerca tra i prodotti nel carrello quelli che necessitano di ricetta
            codice_val = prodotto["codice_farmaco"]
            query = f" SELECT ricetta FROM FarmaciMagazzino WHERE codice = '{codice_val}' AND ricetta = 'si'"
            serve_ricetta = pd.read_sql_query(query, connection)  # può restituire si o rimanere vuoto

            if not serve_ricetta.empty:

                # controllo se l'utente è in possesso della ricetta per acquistare il farmaco
                query = f" SELECT codice_farmaco FROM Ricette WHERE codice_farmaco ='{codice_val}' AND codice_fiscale = '{self.id_utente}'"
                nome_ck = pd.read_sql_query(query, connection)

                if nome_ck.empty:
                    print("Non è associata nessuna ricetta per questo farmaco al profilo corrente, il prodotto con ricetta verrà eliminato dal carrello")
                    carrello.remove(prodotto)
                    del quanto_compro[i]

                if not nome_ck.empty:
                    count += 1
            i += 1
        return count

    def pagare(self, indirizzo: str) -> bool:

        ck: bool
        metodo: str
        prezzo_tot: float = 0
        i: int = 0

        for prodotto in carrello:
            print(f" codice : {prodotto["codice_farmaco"]} ")
            print(f" nome : {prodotto["nome"]} ")
            print(f" quantità : {quanto_compro[i]} ")
            print(f" prezzo : {quanto_compro[i] * float(prodotto["prezzo"])}")
            i += 1

        i = 0
        for prodotto in carrello:
            prezzo_tot = prezzo_tot + float(prodotto["prezzo"]) * quanto_compro[i]
            i += 1

        print(f"Prezzo totale dell'ordine : {prezzo_tot} €")
        print("se si desidera procedere all'acquisto digitare 1")
        print("se si desidera annullare l'operazione digitare exit")
        scelta = input()

        if scelta == "1":
            print("Scegliere metodo di pagamento")
            print("digitare 1 per pagare con carta di credito o debito (American Express, Euro/Mastercard, Visa, Maestro)")
            print("digitare 2 per pagare con portafoglio digitale (paypal , Google pay, Apple pay)")
            metodo = input()

            if metodo == "1":

                print("INSERIMENTO DATI CARTA")
                nome = input("Inserire il nome dell'intestatario : ")
                cognome = input("Inserire il cognome dell'intestatario : ")
                numero_carta = controlla("Inserire numero della carta : ", 16)
                data_scadenza = controlla("Inserire  data di scadenza della carta(gg/mm/aaaa): ", 10)
                cvc = controlla("Inserire il CVC : ", 3)

                print("DATI DELLA CARTA")
                print(f"NOME : {nome}")
                print(f"COGNOME : {cognome}")
                print(f"NUMERO CARTA : {numero_carta}")
                print(f"DATA SCADENZA : {data_scadenza}")
                print(f"CVC : {cvc}")

                ck = check_date(data_scadenza)
                if not ck:
                    print("operazione fallita")#carta scaduta
                    return False
                else:
                    print("operazione andata a buon fine")
                    self.associa_numero_ordine(indirizzo)
                    i = 0
                    for prodotto in carrello:
                        #si modifica la quantità di prodotto in magazzino
                        new_quantity = prodotto["quantità"] - quanto_compro[i]
                        query = f"UPDATE FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{prodotto["codice_farmaco"]}' "
                        connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                        connection.commit()
                        # si elimina la ricetta utilizzata nell'acquisto
                        query = f"DELETE FROM Ricette WHERE codice_farmaco ='{prodotto["codice_farmaco"]}' AND codice_fiscale = '{self.id_utente}' "
                        connection.execute(text(query))
                        connection.commit()
                        i += 1

                    return True

            elif metodo == "2":
                print("operazione andata a buon fine")
                self.associa_numero_ordine(indirizzo)
                i = 0

                for prodotto in carrello:
                    # si modifica la quantità di prodotto in magazzino
                    new_quantity = prodotto["quantità"] - quanto_compro[i]
                    query = f"UPDATE FarmaciMagazzino SET quantità = '{new_quantity}' WHERE codice = '{prodotto["codice_farmaco"]}' "
                    connection.execute(text(query))  # serve per eseguire query che non devono restituire valori
                    connection.commit()
                    # si elimina la ricetta utilizzata nell'acquisto
                    query = f"DELETE FROM Ricette WHERE codice_farmaco ='{prodotto["codice_farmaco"]}' AND codice_fiscale = '{self.id_utente}' "
                    connection.execute(text(query))
                    connection.commit()
                    i += 1
                return True

        elif scelta == "exit":
            return False

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

        scelta: str
        controllo: bool = False
        verifica: str = "1"
        new_quantity: int = 0

        query = "SELECT codice, nome, quantità FROM FarmaciMagazzino WHERE quantità <= 2 "
        riordinare = pd.read_sql(query, connection)

        if not riordinare.empty:
            print("ATTENZIONE!! I seguenti farmaci stanno per terminare o sono già terminati ")
            for farmaco in riordinare.to_dict(orient="records"):
                print(farmaco)
        else:
            return None

        while not controllo:
            print("Se si vuole aggiornare le quantità dei farmaci sopra elencati digitare 1")
            print("Per procedere con altre operazioni digitare 2")
            scelta = input()

            if scelta == "1":

                controllo = True

                while verifica == "1":
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

                        print("Se si desidera continuare ad aggiornare le quantità digitare 1 ")
                        print("Per procedere con altre operazioni digitare 2 ")
                        verifica = input()

                    else:
                        print("Il codice inserito non è presente nella lista fornita , riprovare ")
                        verifica = "1"

            elif scelta == "2":
                return None

            else:
                print("Operazione non valida")
                controllo = False

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

        cod = int(str(cod.iloc[0, 0])) + 1

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

        cod: str
        i: int

        print("Digitare il codice del farmaco che si vuole prescrivere, selezionando dal segunete elenco ")

        query = "SELECT codice , nome FROM FarmaciMagazzino WHERE ricetta = 'si' "
        elenco = pd.read_sql(query, connection)

        if not elenco.empty:
            for farmaco in elenco.to_dict(orient="records"):
                print(farmaco)
        else:
            print("Non ci sono farmaci con ricetta da poter prescrivere in magazzino")

        cod_farmaco = input()
        cod_fisc = input("Inserire il codice fiscale del paziente a cui si sta prescrivendo il farmaco : ")

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


class LavoratoreSanitario (Persona) :#classe base

    t_p: TesserinoProfessionale  # t_p abbreviazione tesserino professionale

    def iscriversi(self) -> bool:
        query = f"SELECT * FROM Sanitari WHERE matricola = '{self.t_p.n_matricola}' AND professione = '{self.t_p.ordine_di_appartenenza}' "
        lav_sani = pd.read_sql(query, connection)
        # si definisce la ricerca da database per controllare se la persona è già registrata
        if not lav_sani.empty:  # è un dataframe
            print("La matricola inserita appartiene a un utente già registrato")

            print("Se si vuole accedere al servizio digitare 1")
            print("Se si vuole ritentare il processo di iscrizione digitare 2")
            print("Digitare exit se si vuole terminare l'operazione")
            scelta = input()

            if scelta == "1":
                return True
            elif scelta == "2":
                self.t_p.n_matricola = input("Inserire il numero di matricola corretto : ")
                return self.iscriversi()
            else:
                return False

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
        nome = input(" inserire un nome utente : ")  # inserire controllo per corrispondenza profilo utente
        password = input(" inserire una password : ")

        profilo = ProfilolavoratoreSanitario(nome, password, self.t_p.n_matricola, self.t_p.ordine_di_appartenenza)

        ck = profilo.controllo_utente()

        while not ck:  # questo nuovo
            nuovo_nome = input("Inserisci un altro nome utente: ")
            profilo.nome_utente = nuovo_nome
            ck = profilo.controllo_utente()

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
        ck : bool
        ck= check_date(self.t_s.data_scadenza) # per verificare che la tessera registrata non sia scaduta

        if ck:
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
            print("La tessera risulta scaduta, non è possibile effettuare l'iscrizione al servizio")
            return False

    def crea_profilo(self) ->bool:

        print("CREAZIONE PROFILO UTENTE")
        nome = input(" inserire un nome utente : ")  # inserire controllo per corrispondenza profilo utente
        password = input(" inserire una password : ")
        profilo = ProfiloCliente(nome, password, self.t_s.codice_fiscale, 'cliente')
        ck = profilo.controllo_utente()

        while not ck:  # questo nuovo
            nuovo_nome = input("Inserisci un altro nome utente: ")
            profilo.nome_utente = nuovo_nome
            ck = profilo.controllo_utente()

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
