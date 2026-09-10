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
Swagger: 
/ordini:
  get:
    summary: Elenco degli ordini
    description: Fornisce un elenco di ordini, opzionalmente filtrato per cliente.
    parameters:
      - in: query
        name: limite
        required: false
        schema:
          type: integer
          example: 20
        description: Numero massimo di ordini da restituire.
      - in: query
        name: cliente
        required: false
        schema:
          type: string
        description: Filtra gli ordini per nome del cliente.
    responses:
      '200':
        description: Elenco ordinato di ordini.
        content:
          application/json:
            schema:
              type: object
              properties:
                ordini:
                  type: array
                totale:
                  type: integer
      '500':
        description: Errore interno del server.
"""
    valori = list(_ordini.values())
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
"""
Swagger: 
/ordini/{ordine_id}:
  get:
    summary: Ottieni un ordine specifico
    description: Restituisce i dettagli di un ordine esistente, identificato dal suo ID.
    parameters:
      - in: path
        name: ordine_id
        required: true
        schema:
          type: string
    responses:
      '200':
        description: Dettagli dell'ordine richiesto.
        content:
          application/json:
            schema:
              type: object
              description: Dati dell'ordine, incluso cliente, articoli e totale.
      '404':
        description: L'ordine richiesto non esiste.
        content:
          application/json:
            schema:
              type: object
              properties:
                detail:
                  type: string
                  example: 'Ordine inesistente'
      '500':
        description: Errore interno del server.
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
"""
Swagger: 
/ordini:
  post:
    summary: Crea un nuovo ordine
    description: Inserisce un ordine nel sistema.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              cliente:
                type: string
              articoli:
                type: array
                items:
                  type: string
              totale:
                type: number
                format: float
    responses:
      '201':
        description: Ordine creato correttamente.
        content:
          application/json:
            schema:
              type: object
              description: Dati dell'ordine appena creato, incluso l'ID univoco generato automaticamente.
      '400':
        description: Richiesta malformata (dati invalidi).
      '500':
        description: Errore interno del server.
"""
    nuovo_id = str(len(_ordini) + 1)
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
"""
Swagger: 
/ordini/{ordine_id}:
  put:
    summary: Sostituisce un ordine
    description: Sostituisce completamente i dati di un ordine esistente con quelli forniti.
    parameters:
      - in: path
        name: ordine_id
        required: true
        schema:
          type: string
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              cliente:
                type: string
              articoli:
                type: array
                items:
                  type: string
              totale:
                type: number
                format: float
    responses:
      '200':
        description: Ordine aggiornato correttamente.
        content:
          application/json:
            schema:
              type: object
      '404':
        description: L'ordine richiesto non esiste.
        content:
          application/json:
            schema:
              type: object
              properties:
                detail:
                  type: string
                  example: 'Ordine inesistente'
      '500':
        description: Errore interno del server.
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
"""
Swagger: 
/ordini/{ordine_id}:
  delete:
    summary: Cancella un ordine
    description: Rimuove un ordine specifico dal sistema.
    parameters:
      - in: path
        name: ordine_id
        required: true
        schema:
          type: string
    responses:
      '204':
        description: Ordine cancellato correttamente senza contenuto restituito.
      '404':
        description: L'ordine richiesto non esiste.
        content:
          application/json:
            schema:
              type: object
              properties:
                detail:
                  type: string
                  example: 'Ordine inesistente'
      '500':
        description: Errore interno del server.
"""
    if _ordini.pop(ordine_id, None) is None:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
"""
Swagger: 
/ordini/{ordine_id}/stato:
  patch:
    summary: Aggiorna lo stato di un ordine
    description: Modifica lo stato di un ordine esistente.
    parameters:
      - in: path
        name: ordine_id
        required: true
        schema:
          type: string
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              stato:
                type: string
    responses:
      '200':
        description: Ordine aggiornato correttamente, incluso il nuovo stato.
        content:
          application/json:
            schema:
              type: object
      '404':
        description: L'ordine richiesto non esiste.
        content:
          application/json:
            schema:
              type: object
              properties:
                detail:
                  type: string
                  example: 'Ordine inesistente'
      '500':
        description: Errore interno del server.
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
