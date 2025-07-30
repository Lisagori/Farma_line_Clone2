from abc import ABC
from profile_creation.base_iscrizioni import *
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

class Persona (ABC) :
    nome: str
    cognome: str

    def __init__(self):
        self.nome = input("Inserire il proprio nome : ")
        self.cognome = input("Inserire il proprio cognome : ")

class TesseraSanitaria :
    codice_fiscale: str
    sesso: str
    luogo_nascita: str
    provincia: str
    data_nascita: str
    data_scadenza: str
    numero_identificazione_tessera: str

    def controllo(self, messaggio: str, lunghezza: int) -> str : #controllo del numero dei caratteri alfanumerici( va aggiunto se si riesce il controllo più specifico o messo come eccezione
       parametro = input(messaggio)
       while len(parametro) != lunghezza :
            parametro = input(f" il parametro non è valido, riprovare : ")
       return parametro

#TODO quando possibile inserire controllo data di nascita e scadenza tessera sanitaria

    def __init__(self):
        print( " Di seguito si inseriscano i dati della tessera sanitaria : ")
        self.codice_fiscale = self.controllo(" CODICE FISCALE :", 16) # nel codice fiscale si contano 16 caratteri alfanumerici
        self.sesso = self.controllo(" SESSO : ", 1)
        self.luogo_nascita = input(" LUOGO DI NASCITA : ")
        self.provincia = self.controllo(" PROVINCIA : ", 2)
        self.data_nascita = self.controllo(" DATA DI NASCITA (gg/mm/aaaa) : ", 10)
        self.data_scadenza = self.controllo(" DATA DI SCADENZA (gg/mm/aaaa) : ", 10)
        self.numero_identificazione_tessera = self.controllo(" NUMERO IDENTIFICAZIONE TESSERA : ", 20)# sulla tessera sanitaria fisica sono 20 caratteri alfanumerici

class Cliente(Persona):
    t_s: TesseraSanitaria #t_s abbreviazione tessera sanitaria

    def __init__(self):
        super().__init__()
        self.t_s = TesseraSanitaria()
    #def ricerca () # da database per controllo su presenza o meno della persona

class TesserinoProfessionale :
    ordine_di_appartenenza: str # indica il settore lavorativo a cui appartieni
    n_matricola : str # indica il numero di iscrizione all'albo di riferimento

    def __init__(self, ordine :str):
        self.ordine_di_appartenenza = ordine
        self.n_iscrizione_albo = input("Inserire il proprio numero di matricola : ")

class Farmacista(Persona):
    t_p: TesserinoProfessionale #t_p abbreviazione tesserino professionale

    def __init__(self):
        super().__init__()
        self.t_p = TesserinoProfessionale("farmacista")
    #def ricerca () # da database per controllo su presenza o meno della persona

class ProfiloUtente :
    nome_utente:str
    password: str
    utente: Persona

    def __init__(self,user : Persona):
        self.utente = user
        self.nome_utente = input(" inserire un nome utente : ") # inserire controllo per corrispondenza profilo utente
        self.password = input(" inserire una password : ")


def iscriversi(user: Persona) -> ProfiloUtente:

    if isinstance(user, Cliente) : # processo di creazione account cliente
        cliente = session.query(ClienteDB).filter_by(codice_fiscale=user.t_s.codice_fiscale).first()

        if cliente:
            print("utente già registrato")
        else:
            profilo = ProfiloUtente(user)
            print(f"""registrazione effettuata con successo.
                     Benvenuto {profilo.nome_utente} ! """)

            # Crea le istanze dei modelli SQLAlchemy da salvare
            tessera = TesseraSanitariaDB(
                codice_fiscale=user.t_s.codice_fiscale,
                sesso=user.t_s.sesso,
                luogo_nascita=user.t_s.luogo_nascita,
                provincia=user.t_s.provincia,
                data_nascita=user.t_s.data_nascita,
                data_scadenza=user.t_s.data_scadenza,
                numero_identificazione_tessera=user.t_s.numero_identificazione_tessera
            )
            session.add(tessera)
            session.commit()

            cliente_db = ClienteDB(
                nome=user.nome,
                cognome=user.cognome,
                codice_fiscale=user.t_s.codice_fiscale
            )
            session.add(cliente_db)
            session.commit()

            return profilo

    elif isinstance(user, Farmacista):  # processo di creazione account farmacista
        farmacista = session.query(FarmacistaDB).filter_by(n_matricola=user.t_p.n_matricola).first()

        if farmacista:
            print("utente già registrato")
        else:
            profilo = ProfiloUtente(user)
            print(f"""registrazione effettuata con successo.
                     Benvenuto {profilo.nome_utente} ! """)

            # Crea le istanze dei modelli SQLAlchemy da salvare
            tessera = TesserinoProfessionaleDB(
                n_matricola=user.t_p.n_matricola,
                ordine_di_appartenenza=user.t_p.ordine_di_appartenenza
            )
            session.add(tessera)
            session.commit()

            farmacista_db = FarmacistaDB(
                nome=user.nome,
                cognome=user.cognome,
                n_matricola=user.t_p.n_matricola
            )
            session.add(farmacista_db)
            session.commit()

            return profilo


#verifica del codice
profile: ProfiloUtente
controllo= int(input(""" Se si desidera iscriversi come cliente digitare 1
Se si desidera iscriversi come farmacista digitare 2 
"""))
if controllo == 1 :
    persona = Cliente()
elif controllo == 2 :
    persona = Farmacista()

print(" profilo cliente ")
profile = iscriversi(persona)