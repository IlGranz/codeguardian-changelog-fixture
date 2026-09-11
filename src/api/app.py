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
"""
Modella un ordine con i relativi dettagli.

Attributes:
    cliente (str): Nome del cliente.
    articoli (list[str]): Lista di articoli nel ordine.
    totale (float): Totale in euro dell'ordine.
"""
    articoli: list[str]
    totale: float


@app.get("/ordini")
def elenca_ordini(limite: int = 20, cliente: str | None = None):
    valori = list(_ordini.values())
"""
Elenca gli ordini filtrati per cliente (opzionale) e limitati in numero.

Args:
    limite (int): numero massimo di ordini restituiti (default: 20).
    cliente (str | None): nome del cliente per il filtro.

Returns:
    dict: un dizionario con la lista di ordini e il totale (senza filtro).
"""
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
    if ordine_id not in _ordini:
"""
Trova un ordine per ID.

Args:
    ordine_id (str): Identificativo univoco dell'ordine da cercare.

Raises:
    HTTPException: 404 se ID inesistente.

Returns:
    dict: Informazioni sull'ordine richiesto se esistente.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
    nuovo_id = str(len(_ordini) + 1)
"""
Genera un nuovo ordine.

Args:
    ordine (Ordine): Dati dell'ordine ricevuti come input.

Returns:
    dict: Informazioni sull'ordine creato comprese l'ID.
"""
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
    if ordine_id not in _ordini:
"""
Completa la sostituzione degli attributi di un ordine esistente.

Args:
    ordine_id (str): Identificativo univoco dell'ordine da sostituire.
    ordine (Ordine): Dati dell'ordine nuovo da aggiornare.

Raises:
    HTTPException: 404 se ID inesistente.

Returns:
    dict: Informazioni sull'ordine aggiornato.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
    if _ordini.pop(ordine_id, None) is None:
"""
Cancella un ordine esistente.

Args:
    ordine_id (str): Identificativo univoco dell'ordine da eliminare.

Raises:
    HTTPException: 404 se ID inesistente.

Returns:
    None
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
    if ordine_id not in _ordini:
"""
Modifica lo stato di un ordine esistente.

Args:
    ordine_id (str): Identificativo univoco dell'ordine da aggiornare.
    stato (str): nuovo stato da assegnare.

Raises:
    HTTPException: 404 se ID inesistente.

Returns:
    dict: Informazioni sull'ordine aggiornato.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
