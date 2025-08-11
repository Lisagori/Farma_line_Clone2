# funzione applicabile a tutte le classi
def controlla(messaggio: str, lunghezza: int) -> str : #controllo del numero dei caratteri alfanumerici( va aggiunto se si riesce il controllo più specifico o messo come eccezione
   parametro = input(messaggio)

   while len(parametro) != lunghezza :
        parametro = input(f" il parametro non è valido, riprovare : ")
   return parametro
