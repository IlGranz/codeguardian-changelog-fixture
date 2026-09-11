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
 * @route GET /clienti
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {string} [req.query.attivi] - Filtra per clienti attivi (true o false)
 * @returns {Object} Elenco dei clienti (filtrato opzionalmente)
 * @response 200 Success - Lista di clienti e numero totale
 */
  const elenco = [...clienti.values()].filter((c) => !soloAttivi || c.attivo);
  res.json({ clienti: elenco, totale: elenco.length });
});

router.get("/clienti/:id", (req: Request, res: Response) => {
  const cliente = clienti.get(req.params.id);
/**
 * @route GET /clienti/:id
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {string} req.params.id - ID univoco del cliente
 * @returns {Object} Dettagli del cliente richiesto o errore 404
 * @response 200 Success - Dettagli del cliente
 * @response 404 Error - Cliente inesistente
 */
  if (!cliente) return res.status(404).json({ errore: "Cliente inesistente" });
  res.json(cliente);
});

router.post("/clienti", (req: Request, res: Response) => {
  const id = String(clienti.size + 1);
/**
 * @route POST /clienti
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {Object} req.body - Dati del cliente da creare
 * @returns {Object} Nuovo cliente creato
 * @response 201 Created - Dettagli del cliente creato
 */
  const cliente: Cliente = { id, ...req.body, attivo: true };
  clienti.set(id, cliente);
  res.status(201).json(cliente);
});

router.delete("/clienti/:id", (req: Request, res: Response) => {
  if (!clienti.delete(req.params.id)) {
/**
 * @route DELETE /clienti/:id
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {string} req.params.id - ID univoco del cliente
 * @returns {Object} Risposta di successo o errore 404
 * @response 204 No Content - Cliente erfolgreich gelöscht
 * @response 404 Error - Cliente inesistente
 */
    return res.status(404).json({ errore: "Cliente inesistente" });
  }
  res.status(204).send();
});
