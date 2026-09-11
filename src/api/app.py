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
---
**Elenca Ordini**

`GET /ordini`

Restituisce lista di ordini filtrati per cliente (opzionale) e limitati in numero. Utile per gestione e analisi ordini.

**Parametri**:
- `limite(int)`: numero massimo di ordini restituiti (default=20)
- `cliente(str | None)`: filtro per cliente

**Risposte**:
- `200`:
  
  ```
  {
    "ordini": List[Ordine],
    "totale": int
  }
  ```

- `400`: Parametri non validi
"""
    valori = list(_ordini.values())
    if cliente:
        valori = [o for o in valori if o["cliente"] == cliente]
    return {"ordini": valori[:limite], "totale": len(valori)}


@app.get("/ordini/{ordine_id}")
def leggi_ordine(ordine_id: str):
"""
---
**Leggi un Ordine**

`GET /ordini/{ordine_id}`

Restituisce l'ordine richiesto tramite ID oppure un errore se non esiste.

**Parametri**:
- `ordine_id(str)`: chiave identificativa unica dell'ordine

**Risposte**:
- `200`:

  ```
  Dict[str, str | float | dict]
  ```

- `404`:

  ```
  {
    "detail": "Ordine inesistente"
  }
  ```
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return _ordini[ordine_id]


@app.post("/ordini", status_code=201)
def crea_ordine(ordine: Ordine):
"""
---
**Crea un Ordine**

`POST /ordini`

Crea un nuovo ordine e restituisce una rappresentazione sua con ID assegnato. Il corpo della richiesta deve rispettare il modello Ordine (Pydantic).

**Parametri Body**:
- `Ordine`:
  ```
  {
    "cliente": str,
    "articoli": list[str],
    "totale": float
  }
  ```

**Risposte**:
- `201`:

  ```
  Dict[str, str | float | dict]
  ```
"""
    nuovo_id = str(len(_ordini) + 1)
    _ordini[nuovo_id] = {"id": nuovo_id, **ordine.model_dump()}
    return _ordini[nuovo_id]


@app.put("/ordini/{ordine_id}")
def sostituisci_ordine(ordine_id: str, ordine: Ordine):
"""
---
**Sostituisce un Ordine**

`PUT /ordini/{ordine_id}`

Aggiorna l'ordine con il contenuto fornito, completo di informazioni. Se non esiste, restituisce errore 404.

**Parametri Body**:
- `Ordine`:
  ```
  {
    "cliente": str,
    "articoli": list[str],
    "totale": float
  }
  ```

**Risposte**:
- `200`:

  ```
  Dict[str, str | float | dict]
  ```

- `404`:

  ```
  {
    "detail": "Ordine inesistente"
  }
  ```
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id] = {"id": ordine_id, **ordine.model_dump()}
    return _ordini[ordine_id]


@app.delete("/ordini/{ordine_id}", status_code=204)
def cancella_ordine(ordine_id: str):
"""
---
**Cancella un Ordine**

`DELETE /ordini/{ordine_id}`

Elimina un ordine specifico identificato da ID. Non restituisce dati se cancellazione avvenuta con successo, o errore se ID errato.

**Parametri**:
- `ordine_id(str)`: chiave identificativa unica dell'ordine

**Risposte**:
- `204`: Nessun contenuto restituito se cancellazione avvenuta con successo

- `404`:

  ```
  {
    "detail": "Ordine inesistente"
  }
  ```
"""
    if _ordini.pop(ordine_id, None) is None:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    return None


@app.patch("/ordini/{ordine_id}/stato")
def aggiorna_stato(ordine_id: str, stato: str):
"""
---
**Aggiorna lo Stato di un Ordine**

`PATCH /ordini/{ordine_id}/stato`

Aggiorna lo stato dell'ordine specificato. Non modifica le informazioni di ordine complete, solo aggiunge o sostituisce "stato".

**Parametri Body**:
- `stato(str)`: nuovo stato da applicare all'ordine

**Parametri**:
- `ordine_id(str)`: chiave identificativa unica dell'ordine

**Risposte**:
- `200`:

  ```
  Dict[str, str | float | dict]
  ```

- `404`:

  ```
  {
    "detail": "Ordine inesistente"
  }
  ```
"""
    if ordine_id not in _ordini:
        raise HTTPException(status_code=404, detail="Ordine inesistente")
    _ordini[ordine_id]["stato"] = stato
    return _ordini[ordine_id]
