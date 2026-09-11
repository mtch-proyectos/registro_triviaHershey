const express = require('express');
const path = require('path');
// Nota: Si usas Node.js 18+, puedes eliminar 'node-fetch' ya que fetch es nativo.
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

// URL de tu Webhook en n8n
const N8N_WEBHOOK_URL = 'https://automatizaciones-n8n-n8n.dy6ey0.easypanel.host/webhook/hershey';

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/api/registro', async (req, res) => {
    // 1. Extraemos score junto con los demás datos
    const { nombre, email, telefono, score, fecha } = req.body;

    // Log para depuración en la consola de Easypanel/Node
    console.log('Registro recibido en backend:', { nombre, email, telefono, score, fecha });

    // 2. Disparo asíncrono a n8n en segundo plano
    (async () => {
        try {
            const response = await fetch(N8N_WEBHOOK_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    nombre,
                    email,
                    telefono,
                    score: score || 0, // Garantiza enviar 0 si viene indefinido
                    fecha: fecha || new Date().toISOString()
                })
            });

            if (!response.ok) {
                console.error(`Error HTTP desde n8n. Estado: ${response.status}`);
            } else {
                console.log('Datos enviados con éxito a n8n');
            }
        } catch (err) {
            console.error('Error de red al conectar con n8n:', err);
        }
    })();

    // 3. Respuesta inmediata al navegador del usuario
    res.status(200).json({ status: 'ok', message: 'Registro recibido correctamente' });
});

app.listen(PORT, () => {
    console.log(`Servidor de registro Hershey's escuchando en puerto ${PORT}`);
});