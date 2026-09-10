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
"""Modello che rappresenta un ordine con cliente, articoli e totale.

Attributes:
    cliente (str): Il nome o l'identificativo del cliente.
    articoli (list[str]): Elenca gli articoli richiesti nell'ordine.
    totale (float): Importo totale dell'ordine.
"""
    articoli: list[str]
    totale: float


@app.get("/ordini")
def elenca_ordini(limite: int = 20, cliente: str | None = None):
    valori = list(_ordini.values())
"""Fornisce un elenco parziale di tutti gli ordini filtrati per cliente se necessario.

Args:
    limite (int, optional): Il numero massimo di ordini da restituire. Predefinito 20.
    cliente (str | None, optional): Filtra gli ordini per utente specifico. Predefinito None.

Returns:
    dict: Informazioni sugli ordini con 'ordini' che è una lista e 'totale' che rappresenta il numero totale di ordini esistenti.
"""
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
    if ordine_id not in _ordini:
"""Recupera un ordine specifico in base all'ID fornito.

Args:
    ordine_id (str): L'identificativo dell'ordine da cercare.

Returns:
    dict: Dettagli dell'ordine richiesto.

Raises:
    HTTPException: Se l'ordine non esiste, viene restituito uno stato 404 con messaggio appropriato.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
    nuovo_id = str(len(_ordini) + 1)
"""Crea un nuovo ordine con gli attributi forniti dal modello.

Args:
    ordine (Ordine): Un modello con i dati dell'ordine da salvare.

Returns:
    dict: Il dettaglio dell'ordine appena creato con un ID generato automaticamente.
"""
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
    if ordine_id not in _ordini:
"""Sostituisce completamente un ordine esistente con i nuovi attributi forniti.

Args:
    ordine_id (str): ID dell'ordine da modificare.
    ordine (Ordine): Nuovi dati dell'ordine da sostituire.

Returns:
    dict: Il dettaglio dell'ordine modificato con nuovi dati.

Raises:
    HTTPException: Se l'ordine specificato non esiste, viene restituito uno stato 404 con messaggio.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
    if _ordini.pop(ordine_id, None) is None:
"""Cancella un ordine esistente in base all'ID fornito.

Args:
    ordine_id (str): ID dell'ordine da cancellare.

Returns:
    None: Nessun contenuto è restituito in caso di cancellazione riuscita (status 204).

Raises:
    HTTPException: Se l'ordine non esiste, restituisce un errore 404.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
    if ordine_id not in _ordini:
"""Aggiorna lo stato di un ordine esistente in base all'ID fornito.

Args:
    ordine_id (str): L'ID dell'ordine da aggiornare.
    stato (str): Nuovo stato da assegnare all'ordine.

Returns:
    dict: Il dettaglio dell'ordine aggiornato con lo stato modificato.

Raises:
    HTTPException: Se l'ordine non esiste, restituisce un errore 404.
"""
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
