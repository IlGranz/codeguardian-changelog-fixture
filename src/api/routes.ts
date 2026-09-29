// Router HTTP di prova per l'Agente Docs API.
//
// Come il modulo Python affiancato, le rotte non hanno commenti JSDoc:
// e' materiale da documentare, non codice in esercizio.

import express, { type Request, type Response } from "express";

export const router = express.Router();

interface Cliente {
  id: string;
  nome: string;
  email: string;
  attivo: boolean;
}

const clienti = new Map<string, Cliente>();

router.get("/clienti", (req: Request, res: Response) => {
  const soloAttivi = req.query.attivi === "true";
/**
 * @title Elenca Clienti
 * @description Recupera un elenco di clienti. Può essere filtrato per stato attivo.
 * @route GET /clienti
 * @query {boolean} [attivi=true] - Indica se mostrare solo clienti attivi
 * @response 200 - Elenco di clienti con totale
 * @schema_response {"clienti": [], "totale": 0}
 * @schema_request {}
 */
  const elenco = [...clienti.values()].filter((c) => !soloAttivi || c.attivo);
  res.json({ clienti: elenco, totale: elenco.length });
});

router.get("/clienti/:id", (req: Request, res: Response) => {
  const cliente = clienti.get(req.params.id);
/**
 * @title Mostra Dettaglio Cliente
 * @description Recupera i dettagli di un cliente per ID.
 * @route GET /clienti/{id}
 * @path {string} id - ID univoco del cliente da recuperare
 * @response 200 - Dettagli del cliente
 * @response 404 - Cliente non trovato
 * @schema_response {"id": "string", "nome": "string", "email": "string", "attivo": "boolean"}
 * @schema_request {}
 * @exception {404} {"errore": "string"} - Cliente inesistente
 */
  if (!cliente) return res.status(404).json({ errore: "Cliente inesistente" });
  res.json(cliente);
});

router.post("/clienti", (req: Request, res: Response) => {
  const id = String(clienti.size + 1);
/**
 * @title Crea Cliente
 * @description Crea un nuovo cliente.
 * @route POST /clienti
 * @body {object} - Dati del cliente da creare
 * @body {string} id - ID automatico (sarà generato dal sistema)
 * @body {string} nome - Nome del cliente
 * @body {string} email - Email del cliente
 * @body {boolean} attivo - Stato attivo del cliente
 * @response 201 - Dati del cliente appena creato
 * @schema_response {"id": "string", "nome": "string", "email": "string", "attivo": "boolean"}
 * @schema_request {"nome": "string", "email": "string"}
 */
  const cliente: Cliente = { id, ...req.body, attivo: true };
  clienti.set(id, cliente);
  res.status(201).json(cliente);
});

router.delete("/clienti/:id", (req: Request, res: Response) => {
  if (!clienti.delete(req.params.id)) {
/**
 * @title Cancella Cliente
 * @description Cancella un cliente per ID.
 * @route DELETE /clienti/{id}
 * @path {string} id - ID del cliente da cancellare
 * @response 204 - Cliente cancellato senza contenuto
 * @response 404 - Cliente non trovato
 * @schema_request {} 
 * @schema_response {} 
 * @exception {404} {"errore": "string"} - Cliente inesistente
 */
    return res.status(404).json({ errore: "Cliente inesistente" });
  }
  res.status(204).send();
});
