from abc import ABC, abstractmethod

from classi.persone.classe_profilo import ProfiloUtente
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