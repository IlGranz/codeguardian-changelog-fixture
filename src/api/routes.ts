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
 * 
 * @swagger
 * /clienti:
 *   get:
 *     summary: Elenco dei clienti (filtrabile per stato attivo).
 *     parameters:
 *       - in: query
 *         name: attivi
 *         schema:
 *           type: string
 *         description: Se "true", solo clienti attivi saranno restituiti.
 *     responses:
 *       200:
 *         description: Lista di clienti.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 clienti:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Cliente'
 *                 totale:
 *                   type: integer
 *       400:
 *         description: Parametro non valido.
 */
  const elenco = [...clienti.values()].filter((c) => !soloAttivi || c.attivo);
  res.json({ clienti: elenco, totale: elenco.length });
});

router.get("/clienti/:id", (req: Request, res: Response) => {
  const cliente = clienti.get(req.params.id);
/**
 * 
 * @swagger
 * /clienti/{id}:
 *   get:
 *     summary: Recupera un cliente specifico tramite ID.
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Dettagli del cliente.
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Cliente'
 *       404:
 *         description: Cliente non esistente.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 errore:
 *                   type: string
 */
  if (!cliente) return res.status(404).json({ errore: "Cliente inesistente" });
  res.json(cliente);
});

router.post("/clienti", (req: Request, res: Response) => {
  const id = String(clienti.size + 1);
/**
 * 
 * @swagger
 * /clienti:
 *   post:
 *     summary: Crea un nuovo cliente.
 *     parameters:
 *       - in: body
 *         name: cliente
 *         required: true
 *         schema:
 *           $ref: '#/components/schemas/Cliente'
 *     responses:
 *       201:
 *         description: Cliente creato con successo.
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Cliente'
 *       400:
 *         description: Parametro in corpo non conforme.
 */
  const cliente: Cliente = { id, ...req.body, attivo: true };
  clienti.set(id, cliente);
  res.status(201).json(cliente);
});

router.delete("/clienti/:id", (req: Request, res: Response) => {
  if (!clienti.delete(req.params.id)) {
/**
 * 
 * @swagger
 * /clienti/{id}:
 *   delete:
 *     summary: Cancella un cliente tramite ID.
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       204:
 *         description: Cliente rimosso.
 *       404:
 *         description: Cliente non esistente.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 errore:
 *                   type: string
 */
    return res.status(404).json({ errore: "Cliente inesistente" });
  }
  res.status(204).send();
});
