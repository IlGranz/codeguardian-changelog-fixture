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
 * @swagger
 * /clienti:
 *   get:
 *     summary: Elenco clienti
 *     description: Ritorna l'elenco di tutti i clienti o un subset filtrato solo sui clienti attivi.
 *     parameters:
 *       - in: query
 *         name: attivi
 *         schema:
 *           type: boolean
 *           example: true
 *         description: Filtra gli elenchi per clienti attivi (true) o tutti (false). Opcionalmente puo` essere assente, in tal caso vengono forniti solo i clienti attivi.
 *     responses:
 *       200:
 *         description: Elenco dei clienti (filtrati o no, in base al parametro `attivi`).
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
 *                   description: Totale clienti trovati (senza limiti di filtri).
 *       500:
 *         description: Errore interno del server.
 */
  const elenco = [...clienti.values()].filter((c) => !soloAttivi || c.attivo);
  res.json({ clienti: elenco, totale: elenco.length });
});

router.get("/clienti/:id", (req: Request, res: Response) => {
  const cliente = clienti.get(req.params.id);
/**
 * @swagger
 * /clienti/{id}:
 *   get:
 *     summary: Dettagli cliente
 *     description: Ritorna i dettagli di un cliente specifico identificato dal suo ID.
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
 *                   example: 'Cliente inesistente'
 *       500:
 *         description: Errore interno del server.
 */
  if (!cliente) return res.status(404).json({ errore: "Cliente inesistente" });
  res.json(cliente);
});

router.post("/clienti", (req: Request, res: Response) => {
  const id = String(clienti.size + 1);
/**
 * @swagger
 * /clienti:
 *   post:
 *     summary: Crea un nuovo cliente
 *     description: Crea un nuovo cliente con id generato automaticamente e stato iniziale di attivo: true.
 *     parameters:
 *       - in: body
 *         name: cliente
 *         required: true
 *         schema:
 *           $ref: '#/components/schemas/Cliente'
 *         description: Oggetto cliente da creare. Si assume che l'oggetto non contenga l'
 *     responses:
 *       201:
 *         description: Nuovo cliente creato con successo.
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Cliente'
 *       400:
 *         description: Richiesta malformata - dati invalidi forniti nel corpo della richiesta.
 *       500:
 *         description: Errore interno del server.
 */
  const cliente: Cliente = { id, ...req.body, attivo: true };
  clienti.set(id, cliente);
  res.status(201).json(cliente);
});

router.delete("/clienti/:id", (req: Request, res: Response) => {
  if (!clienti.delete(req.params.id)) {
/**
 * @swagger
 * /clienti/{id}:
 *   delete:
 *     summary: Cancella un cliente
 *     description: Rimuove un cliente specifico identificato pelo suo ID.
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       204:
 *         description: Cliente cancellato correttamente.
 *       404:
 *         description: Cliente non trovato. Nessun oggetto cancellato.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 errore:
 *                   type: string
 *                   example: 'Cliente inesistente'
 *       500:
 *         description: Errore interno del server.
 */
    return res.status(404).json({ errore: "Cliente inesistente" });
  }
  res.status(204).send();
});
