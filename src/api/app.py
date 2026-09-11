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
"""Modello che rappresenta un ordine, inclusi i dati principali.

Attributes:
    cliente (str): Nome del cliente associato all'ordine.
    articoli (list[str]): Lista degli articoli ordinati.
    totale (float): Totale in euro dell'ordine.
"""
    articoli: list[str]
    totale: float


@app.get("/ordini")
def elenca_ordini(limite: int = 20, cliente: str | None = None):
    valori = list(_ordini.values())
"""Restituisce una lista di ordini, opzionalmente filtrata per cliente.

Args:
    limite (int): Massimo numero di ordini da restituire (default: 20).
    cliente (str | None): Filtro per il nome del cliente (opzionale).

Returns:
    dict: Dizionario contenente 'ordini' (lista filtrata) e 'totale' (numero totale di ordini).
"""
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
    if ordine_id not in _ordini:
"""Ottiene i dettagli di un ordine specifico in base all'ID.

Args:
    ordine_id (str): Identificatore univoco dell'ordine.

Returns:
    dict: Dati completi dell'ordine richiesto.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce 404 con messaggio di errore.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
    nuovo_id = str(len(_ordini) + 1)
"""Crea un nuovo ordine in base alle informazioni fornite.

Args:
    ordine (Ordine): Dati dell'ordine da creare.

Returns:
    dict: Dati dell'ordine appena creato, incluso l'ID assegnato automaticamente.
"""
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
    if ordine_id not in _ordini:
"""Sostituisce i dati di un ordine esistente con quelli forniti.

Args:
    ordine_id (str): Identificatore univoco dell'ordine da sostituire.
    ordine (Ordine): Nuovi dati dell'ordine da sovrascrivere.

Returns:
    dict: Dati aggiornati dell'ordine.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce 404 con messaggio di errore.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
    if _ordini.pop(ordine_id, None) is None:
"""Elimina l'ordine corrispondente all'ID fornito.

Args:
    ordine_id (str): Identificatore univoco dell'ordine da cancellare.

Returns:
    None: Nessun contenuto restituito in risposta.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce 404 con messaggio di errore.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
    if ordine_id not in _ordini:
"""Aggiorna lo stato di un ordine esistente.

Args:
    ordine_id (str): Identificatore univoco dell'ordine da aggiornare.
    stato (str): Nuovo stato da assegnare all'ordine.

Returns:
    dict: Dati aggiornati, incluso il nuovo stato.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce 404 con messaggio di errore.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
