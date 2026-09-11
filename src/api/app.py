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
"""
@GetMapping("/ordini")
@return schema:
  $200: dict[str, list[Ordine]] & {"totale": int}
  $400: str
  $500: str
$query_params:
  - name: limite
    type: int
  - name: cliente
    type: str | None
"""
    valori = list(_ordini.values())
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
"""
@GetMapping("/ordini/{ordine_id}")
@return schema:
  $200: Ordine
  $404: str
$path_params:
  - name: ordine_id
    type: str
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
"""
@Post("/ordini")
@return schema:
  $201: Ordine
$request_body:
  - name: ordine
    type: Ordine
"""
    nuovo_id = str(len(_ordini) + 1)
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
"""
@Put("/ordini/{ordine_id}")
@return schema:
  $200: Ordine
  $404: str
$path_params:
  - name: ordine_id
    type: str
$request_body:
  - name: ordine
    type: Ordine
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
"""
@Delete("/ordini/{ordine_id}")
@return schema:
  $204: None
  $404: str
$path_params:
  - name: ordine_id
    type: str
"""
    if _ordini.pop(ordine_id, None) is None:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
"""
@Patch("/ordini/{ordine_id}/stato")
@return schema:
  $200: Ordine
  $404: str
$path_params:
  - name: ordine_id
    type: str
$request_body:
  - name: stato
    type: str
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
