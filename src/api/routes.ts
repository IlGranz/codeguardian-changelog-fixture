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
  const elenco = [...clienti.values()].filter((c) => !soloAttivi || c.attivo);
  res.json({ clienti: elenco, totale: elenco.length });
});

router.get("/clienti/:id", (req: Request, res: Response) => {
  const cliente = clienti.get(req.params.id);
  if (!cliente) return res.status(404).json({ errore: "Cliente inesistente" });
  res.json(cliente);
});

router.post("/clienti", (req: Request, res: Response) => {
  const id = String(clienti.size + 1);
  const cliente: Cliente = { id, ...req.body, attivo: true };
  clienti.set(id, cliente);
  res.status(201).json(cliente);
});

router.delete("/clienti/:id", (req: Request, res: Response) => {
  if (!clienti.delete(req.params.id)) {
    return res.status(404).json({ errore: "Cliente inesistente" });
  }
  res.status(204).send();
});
