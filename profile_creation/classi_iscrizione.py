from abc import ABC, abstractmethod
from profile_creation.base_iscrizione import *
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

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
    def iscriversi(self):
        ...

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
            prf = ProfiloUtenteDB(  # prf fa riferimento al profilo utente da associare alla relativa tebella
                nome_utente=self.nome_utente,
                password=self.password,
                id_cliente=self.utente.t_s.codice_fiscale
            )
        elif isinstance(self.utente, Farmacista):
            prf = ProfiloUtenteDB(
                nome_utente=self.nome_utente,
                password=self.password,
                id_farmacista=self.utente.t_p.n_matricola
            )
        else:
            prf = ProfiloUtenteDB()
            print(" il processo di associazione profilo non è andato a buon fine ")
        session.add(prf)
        session.commit()
        return None

    def controllo(self)->bool:
        profilo_esistente = session.query(ProfiloUtenteDB).filter_by(nome_utente=self.nome_utente).first()
        if profilo_esistente:
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
        # Crea le istanze dei modelli SQLAlchemy da salvare sulle tabelle
        tessera = TesseraSanitariaDB(
            codice_fiscale=self.codice_fiscale,
            sesso=self.sesso,
            luogo_nascita=self.luogo_nascita,
            provincia=self.provincia,
            data_nascita=self.data_nascita,
            data_scadenza=self.data_scadenza,
            numero_identificazione_tessera=self.numero_identificazione_tessera
        )

        session.add(tessera)
        session.commit()

class TesserinoProfessionale :
    ordine_di_appartenenza: str # indica il settore lavorativo a cui appartieni
    n_matricola : str # indica il numero di iscrizione all'albo di riferimento

    def __init__(self, ordine :str):
        self.ordine_di_appartenenza = ordine
        self.n_matricola = input("Inserire il proprio numero di matricola : ")

    def associazione_tessera_a_db(self):
        # Crea le istanze dei modelli SQLAlchemy da salvare sulle tabelle

        tessera = TesserinoProfessionaleDB(
            n_matricola=self.n_matricola,
            ordine_di_appartenenza=self.ordine_di_appartenenza
        )

        session.add(tessera)
        session.commit()

class Cliente(Persona):
    t_s: TesseraSanitaria #t_s abbreviazione tessera sanitaria

    def __init__(self):
        super().__init__()
        self.t_s = TesseraSanitaria()

    def iscriversi(self):
        cliente = session.query(ClienteDB).filter_by(codice_fiscale=self.t_s.codice_fiscale).first()   #si definisce la ricerca da database per controllare se la persona è già registrata

        if cliente:
            print("Il codice fiscale inserito appartiene a un utente già registrato")
        else:
            self.t_s.associazione_tessera_a_db()

            cliente_db = ClienteDB(
                nome=self.nome,
                cognome=self.cognome,
                codice_fiscale=self.t_s.codice_fiscale
            )

            session.add(cliente_db)
            session.commit()
            profilo = ProfiloUtente(self)
            ck = profilo.controllo()
            while not ck: #questo nuovo
                    nuovo_nome = input("Inserisci un altro nome utente: ")
                    profilo.nome_utente = nuovo_nome
                    ck = profilo.controllo()

            profilo.associazione_profilo_utente() #quest è giusto
            print(f"""registrazione effettuata con successo.
            Benvenuto {profilo.nome_utente} ! """)

            #sezione per associazione profilo utente

class Farmacista(Persona):
    t_p: TesserinoProfessionale #t_p abbreviazione tesserino professionale

    def __init__(self):
        super().__init__()
        self.t_p = TesserinoProfessionale("farmacista")

    def iscriversi(self):
        farmacista = session.query(FarmacistaDB).filter_by(matricola=self.t_p.n_matricola).first() # si definisce la ricerca da database per controllare se la persona è già registrata

        if farmacista:
            print("La matricola inserita appartiene a un utente già registrato")
        else:
            self.t_p.associazione_tessera_a_db()

            farmacista_db = FarmacistaDB(
                nome=self.nome,
                cognome=self.cognome,
                matricola=self.t_p.n_matricola
            )
            session.add(farmacista_db)
            session.commit()

            profilo = ProfiloUtente(self)
            ck = profilo.controllo()
            while not ck:  # questo nuovo
                nuovo_nome = input("Inserisci un altro nome utente: ")
                profilo.nome_utente = nuovo_nome
                ck = profilo.controllo()

            profilo.associazione_profilo_utente()

            print(f"""registrazione effettuata con successo.
            Benvenuto {profilo.nome_utente} ! """)


