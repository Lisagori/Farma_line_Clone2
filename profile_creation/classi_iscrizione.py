from abc import ABC, abstractmethod
import pandas as pd
from db import connection

# funzione applicabile a tutte le classi
def controlla(messaggio: str, lunghezza: int) -> str : #controllo del numero dei caratteri alfanumerici( va aggiunto se si riesce il controllo più specifico o messo come eccezione
   parametro = input(messaggio)

   while len(parametro) != lunghezza :
        parametro = input(f" il parametro non è valido, riprovare : ")
   return parametro

class Persona (ABC) :
    nome: str
    cognome: str

    def __init__(self):
        self.nome = input("Inserire il proprio nome : ")
        self.cognome = input("Inserire il proprio cognome : ")

    @abstractmethod
    def iscriversi(self) -> bool:
        ...

    def crea_profilo(self) ->bool:

        profilo = ProfiloUtente(self)
        ck = profilo.controllo_utente()
        while not ck:  # questo nuovo
            nuovo_nome = input("Inserisci un altro nome utente: ")
            profilo.nome_utente = nuovo_nome
            ck = profilo.controllo_utente()

        profilo.associazione_profilo_utente()

        print("registrazione effettuata con successo.")
        print(f"        Benvenuto {profilo.nome_utente} !")
        return True

class ProfiloUtente :
    nome_utente:str
    password: str
    utente: Persona

    def __init__(self,user : Persona):
        self.utente = user
        self.nome_utente = input(" inserire un nome utente : ") # inserire controllo per corrispondenza profilo utente
        self.password = input(" inserire una password : ")

    def associazione_profilo_utente(self) -> None:

        if isinstance(self.utente, Cliente):
            new_profile= pd.DataFrame ( # prf fa riferimento al profilo utente da associare alla relativa tebella
                    columns=['nome_utente','password','id_cliente'],
                data= [
                    [self.nome_utente,self.password,self.utente.t_s.codice_fiscale]
                ]
            )
            new_profile.to_sql('ProfiloUtente', connection, if_exists='append', index=False)
            connection.commit()

        elif isinstance(self.utente, Farmacista):
            new_profile = pd.DataFrame(  # prf fa riferimento al profilo utente da associare alla relativa tebella
                columns=['nome_utente','password','id_farmacista'],
                data=[
                [self.nome_utente, self.password, self.utente.t_p.n_matricola]
                ]
            )
            new_profile.to_sql('ProfiloUtente', connection, if_exists='append', index=False)
            connection.commit()
        else:
            print("  Associazione profilo fallita: tipo utente non valido.")
            return #TODO CONTROLLARE COSA RESTITUISCE

        print("Profilo utente aggiunto con successo.")
        return None

    def controllo_utente(self)->bool:
        query = f"SELECT * FROM ProfiloUtente WHERE nome_utente = '{self.nome_utente}'"
        profilo_esistente = pd.read_sql(query, connection)
        if not profilo_esistente.empty: #pd.read_sql(...) restituisce sempre un DataFrame di pandas.
            print(f"Il nome utente '{self.nome_utente}' è già in uso. Scegliere un altro nome.")
            return False
        else:
            return True

class TesseraSanitaria :
    codice_fiscale: str
    sesso: str
    luogo_nascita: str
    provincia: str
    data_nascita: str
    data_scadenza: str
    numero_identificazione_tessera: str

    #TODO quando possibile inserire controllo data di nascita e scadenza tessera sanitaria

    def __init__(self):
        print( " Di seguito si inseriscano i dati della tessera sanitaria : ")
        self.codice_fiscale = controlla(" CODICE FISCALE :", 16) # nel codice fiscale si contano 16 caratteri alfanumerici
        self.sesso = controlla(" SESSO : ", 1)
        self.luogo_nascita = input(" LUOGO DI NASCITA : ")
        self.provincia = controlla(" PROVINCIA : ", 2)
        self.data_nascita = controlla(" DATA DI NASCITA (gg/mm/aaaa) : ", 10)
        self.data_scadenza = controlla(" DATA DI SCADENZA (gg/mm/aaaa) : ", 10)
        self.numero_identificazione_tessera = controlla(" NUMERO IDENTIFICAZIONE TESSERA : ", 20)# sulla tessera sanitaria fisica sono 20 caratteri alfanumerici

    def associazione_tessera_a_db(self):
        new_tessera = pd.DataFrame(
            [[
                self.codice_fiscale,
                self.sesso,
                self.luogo_nascita,
                self.provincia,
                self.data_nascita,
                self.data_scadenza,
                self.numero_identificazione_tessera
            ]],
            columns=[
                'codice_fiscale',  # <-- niente spazio finale
                'sesso',
                'luogo_nascita',
                'provincia',
                'data_nascita',
                'data_scadenza',
                'numero_identificazione_tessera'
            ]
        )
        new_tessera.to_sql('TesseraSanitaria', connection, if_exists='append', index=False)
        connection.commit()

class TesserinoProfessionale :
    ordine_di_appartenenza: str # indica il settore lavorativo a cui appartieni
    n_matricola : str # indica il numero di iscrizione all'albo di riferimento

    def __init__(self, ordine :str):
        self.ordine_di_appartenenza = ordine
        self.n_matricola = input("Inserire il proprio numero di matricola : ")

    def associazione_tessera_a_db(self):
        # Crea le istanze dei modelli SQLAlchemy da salvare sulle tabelle
        new_tesserino = pd.DataFrame(
            columns=['ordine_appartenenza','n_matricola'],
            data=[
            [self.ordine_di_appartenenza, self.n_matricola]
            ]
        )
        new_tesserino.to_sql('TesserinoProfessionale', connection, if_exists='append', index=False)
        connection.commit()

class Cliente(Persona):
    t_s: TesseraSanitaria #t_s abbreviazione tessera sanitaria

    def __init__(self):
        super().__init__()
        self.t_s = TesseraSanitaria()

    def iscriversi(self) -> bool:
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

class Farmacista(Persona):
    t_p: TesserinoProfessionale #t_p abbreviazione tesserino professionale

    def __init__(self):
        super().__init__()
        self.t_p = TesserinoProfessionale("farmacista")

    def iscriversi(self) ->bool :
        query = f"SELECT * FROM Farmacista WHERE matricola = '{self.t_p.n_matricola}'"
        farmacista = pd.read_sql(query, connection)
        # si definisce la ricerca da database per controllare se la persona è già registrata
        if not farmacista.empty: #è un dataframe
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
            new_farmacista = pd.DataFrame(
                columns=['nome','cognome','matricola'],
                data=[
                [self.nome, self.cognome, self.t_p.n_matricola]
                ]
            )
            new_farmacista.to_sql('Farmacista', connection, if_exists='append', index=False)
            connection.commit()
            # sezione per associazione profilo utente
            return self.crea_profilo()