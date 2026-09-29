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
    articoli: list[str]
    totale: float


@app.get("/ordini")
def elenca_ordini(limite: int = 20, cliente: str | None = None):
'''
# @title Elenca Ordini
# @description Recupera un elenco parziale di ordini (opzionalmente filtrati per cliente).
# @route GET /ordini
# @param {int} limite - numero massimo di ordini restituiti. Default: 20
# @param {str|None} cliente - filtra gli ordini per il cliente specificato
# @response 200 - Lista di ordini con il totale
# @response 400 - Parametri non validi
# @schema_response {"ordini": [], "totale": 0}
# @schema_request {}
'''
    valori = list(_ordini.values())
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
'''    
# @title Leggi Ordine
# @description Recupera i dettagli di un ordine specifico tramite ID.
# @route GET /ordini/{ordine_id}
# @param {str} ordine_id - ID dell'ordine
# @response 200 - Dettagli dell'ordine
# @response 404 - Ordine non esistente
# @schema_response {"id": "", "cliente": "", "articoli": [], "totale": 0.0}
# @schema_request {} 
# @exception {HTTPException} 404: Ordine inesistente
'''
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
''' 
# @title Crea Ordine
# @description Crea un nuovo ordine e lo restituisce con l'ID assegnato.
# @route POST /ordini
# @response 201 - Dati del nuovo ordine con ID assegnato
# @schema_body {"cliente": "", "articoli": [], "totale": 0.0}
# @schema_response {"id": "", "cliente": "", "articoli": [], "totale": 0.0}
# @schema_request {"cliente": "string", "articoli": ["string"], "totale": "number"} 
'''
    nuovo_id = str(len(_ordini) + 1)
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
''' 
# @title Sostituisci Ordine
# @description Sostituisce un ordine esistente con nuovi dati.
# @route PUT /ordini/${ordine_id}
# @param {str} ordine_id - ID dell'ordine da aggiornare
# @response 200 - Ordine aggiornato
# @response 404 - Ordine non esistente
# @schema_body {"cliente": "", "articoli": [], "totale": 0.0}
# @schema_response {"id": "", "cliente": "", "articoli": [], "totale": 0.0}
# @schema_request {"cliente": "string", "articoli": ["string"], "totale": "number"} 
# @exception {HTTPException} 404: Ordine inesistente
'''
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
''' 
# @title Cancella Ordine
# @description Cancella un ordine esistente tramite ID.
# @route DELETE /ordini/{ordine_id}
# @param {str} ordine_id - ID dell'ordine da cancellare
# @response 204 - Indica che l'ordine e' stato cancellato senza contenuto
# @response 404 - Ordine non esistente
# @param {str} ordine_id - ID dell'ordine
# @schema_request {} 
# @exception {HTTPException} 404: Ordine inesistente
'''
    if _ordini.pop(ordine_id, None) is None:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
''' 
# @title Aggiorna Stato Ordine
# @description Aggiorna lo stato di un ordine esistente.
# @route PATCH /ordini/{ordine_id}/stato
# @param {str} ordine_id - ID dell'ordine da aggiornare
# @param {str} stato - nuovo stato dell'ordine
# @response 200 - Dati aggiornati dell'ordine
# @response 404 - Ordine non esistente
# @schema_response {"id": "", "cliente": "", "articoli": [], "totale": 0.0, "stato": "string"}
# @schema_request {"stato": "string"}
# @exception {HTTPException} 404: Ordine inesistente
'''
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
