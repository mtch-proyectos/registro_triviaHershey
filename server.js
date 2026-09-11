const express = require('express');
const path = require('path');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

// Reemplaza con la URL del Webhook Trigger de tu n8n
const N8N_WEBHOOK_URL = 'https://automatizaciones-n8n-n8n.dy6ey0.easypanel.host/webhook/hershey';

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/api/registro', async (req, res) => {
    const { nombre, email, telefono, fecha } = req.body;

    // Disparo asíncrono a n8n
    fetch(N8N_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, email, telefono, fecha })
    }).catch(err => console.error("Error al enviar a n8n:", err));

    res.status(200).json({ status: 'ok' });
});

app.listen(PORT, () => {
    console.log(`Servidor de registro Hershey's escuchando en puerto ${PORT}`);
});