"""Servizio HTTP di prova per l'Agente Docs API.

Gli endpoint qui sotto sono deliberatamente privi di docstring: servono a
dare all'agente qualcosa da documentare. Il modulo non e' in esecuzione da
nessuna parte, e' materiale da leggere.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Fixture API")

_ordini: dict[str, dict] = {}


class Ordine(BaseModel):
    cliente: str
"""Modello che rappresenta un ordine.

Attributes:
    cliente (str): Nome del cliente associato all'ordine.
    articoli (list[str]): Elenco degli articoli nell'ordine.
    totale (float): Importo totale dell'ordine.
"""
    articoli: list[str]
    totale: float


@app.get("/ordini")
def elenca_ordini(limite: int = 20, cliente: str | None = None):
    valori = list(_ordini.values())
"""Restituisce elenco degli ordini filtrati e limitati.

Args:
    limite (int): Numero massimo di ordini da restituire. Default a 20.
    cliente (str | None): Filtra gli ordini per cliente specifico. Default a None.

Returns:
    dict: Dizionario con lista di ordini e numero totale.
"""
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
    if ordine_id not in _ordini:
"""Restituisce dettagli di un ordine specifico.

Args:
    ordine_id (str): Identificativo unico dell'ordine da recuperare.

Returns:
    dict: Dati dell'ordine.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce codice 404.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
    nuovo_id = str(len(_ordini) + 1)
"""Crea un nuovo ordine e lo assegna un ID automatico.

Args:
    ordine (Ordine): Gli attributi dell'ordine da creare.

Returns:
    dict: Informazioni aggiornate sull'ordine creato.
"""
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
    if ordine_id not in _ordini:
"""Sostituisce un ordine esistente con nuovi dati.

Args:
    ordine_id (str): Identificativo dell'ordine da sostituire.
    ordine (Ordine): Dati dell'ordine da aggiornare.

Returns:
    dict: Dati dell'ordine aggiornato.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce codice 404.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
    if _ordini.pop(ordine_id, None) is None:
"""Cancella un ordine esistente.

Args:
    ordine_id (str): Identificativo dell'ordine da eliminare.

Returns:
    None: Nessun contenuto restituito se riuscita.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce codice 404.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
    if ordine_id not in _ordini:
"""Aggiorna lo stato di un ordine esistente.

Args:
    ordine_id (str): Identificativo dell'ordine da aggiornare.
    stato (str): Nuovo stato da assegnare all'ordine.

Returns:
    dict: Ordine aggiornato con lo stato nuovo.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce codice 404.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
