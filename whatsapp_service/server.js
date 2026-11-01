const express = require('express');
const cors = require('cors');
const path = require('path');
const axios = require('axios');
const qrcode = require('qrcode');
const pino = require('pino');
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');

const PORT = process.env.PORT || 8085;
const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000';
const SUPPLIER_NUMBER = (process.env.SUPPLIER_NUMBER || '5511999999999').replace(/\D/g, '');

const app = express();
app.use(cors());
app.use(express.json());

let sock = null;
let connectionStatus = 'init'; // 'init' | 'qr_ready' | 'connecting' | 'connected' | 'disconnected'
let latestQr = null;
let qrImage = null;
let userInfo = null;

// Normaliza números brasileiros para JID do WhatsApp
function formatJid(number) {
    if (!number) return null;
    let clean = number.toString().replace(/\D/g, '');
    if (clean.length === 10 || clean.length === 11) {
        clean = '55' + clean;
    }
    return `${clean}@s.whatsapp.net`;
}

async function startWhatsApp() {
    connectionStatus = 'connecting';
    const authDir = path.join(__dirname, 'auth_info_baileys');
    const { state, saveCreds } = await useMultiFileAuthState(authDir);

    sock = makeWASocket({
        auth: state,
        printQRInTerminal: false,
        logger: pino({ level: 'silent' }),
        browser: ['Viditex Distribuidora', 'Chrome', '1.0.0']
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            latestQr = qr;
            qrImage = await qrcode.toDataURL(qr);
            connectionStatus = 'qr_ready';
            console.log('\n======================================================');
            console.log(' [WhatsApp] NOVO QR CODE GERADO!');
            console.log(` Abra no navegador: http://localhost:${PORT}/qrcode`);
            console.log(' Ou escaneie direto do terminal abaixo:');
            console.log('======================================================\n');
            qrcode.toString(qr, { type: 'terminal', small: true }, (err, str) => {
                if (!err) console.log(str);
            });
        }

        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode || lastDisconnect?.error?.status;
            const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
            console.log(`[WhatsApp] Conexão encerrada (código ${statusCode}). Reconectando: ${shouldReconnect}`);
            connectionStatus = 'disconnected';
            userInfo = null;

            if (shouldReconnect) {
                setTimeout(startWhatsApp, 3000);
            } else {
                console.log('[WhatsApp] Desconectado permanentemente (logout).');
                connectionStatus = 'logged_out';
            }
        } else if (connection === 'open') {
            connectionStatus = 'connected';
            latestQr = null;
            qrImage = null;
            userInfo = sock.user;
            console.log('\n======================================================');
            console.log(' [WhatsApp] CONECTADO COM SUCESSO! ✅');
            console.log(` Número conectado: ${sock.user?.id}`);
            console.log('======================================================\n');
        }
    });

    // Encaminha mensagens recebidas para os webhooks do FastAPI
    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        for (const msg of messages) {
            if (!msg.message || msg.key.fromMe) continue;
            const remoteJid = msg.key.remoteJid;
            if (!remoteJid || remoteJid.includes('@g.us') || remoteJid.includes('status@broadcast')) continue;

            const number = remoteJid.replace('@s.whatsapp.net', '');
            const text = msg.message.conversation ||
                         msg.message.extendedTextMessage?.text ||
                         msg.message.imageMessage?.caption ||
                         msg.message.documentMessage?.caption || '';

            if (!text.trim()) continue;

            const payload = {
                message_id: msg.key.id,
                number: number,
                text: text.trim(),
                is_group: false
            };

            const isSupplier = SUPPLIER_NUMBER && (number.includes(SUPPLIER_NUMBER) || SUPPLIER_NUMBER.includes(number));
            const webhookUrl = isSupplier
                ? `${FASTAPI_URL}/api/v1/webhooks/whatsapp/supplier`
                : `${FASTAPI_URL}/api/v1/webhooks/whatsapp/customer`;

            console.log(`[WhatsApp Inbound] De ${number} (${isSupplier ? 'FORNECEDOR' : 'CLIENTE'}): "${payload.text}"`);

            try {
                await axios.post(webhookUrl, payload, { timeout: 10000 });
                console.log(`[WhatsApp Inbound] Encaminhado com sucesso para ${webhookUrl}`);
            } catch (err) {
                console.warn(`[WhatsApp Inbound] Aviso: FastAPI (${webhookUrl}) não respondeu: ${err.message}`);
            }
        }
    });
}

// Status JSON
app.get('/status', (req, res) => {
    res.json({
        status: connectionStatus,
        user: userInfo,
        hasQr: !!qrImage
    });
});

app.get('/qr-data', (req, res) => {
    res.json({
        status: connectionStatus,
        qrImage: qrImage,
        user: userInfo
    });
});

// Página HTML amigável para escanear o QR Code
app.get('/qrcode', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Conexão WhatsApp - Viditex Distribuidora</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0f172a;
      color: #f8fafc;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 20px;
      padding: 36px;
      max-width: 480px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    }
    h1 {
      font-size: 24px;
      color: #38bdf8;
      margin-bottom: 8px;
    }
    p.sub {
      color: #94a3b8;
      font-size: 14px;
      margin-bottom: 24px;
    }
    .badge {
      display: inline-block;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      margin-bottom: 20px;
    }
    .badge-connecting { background: #854d0e; color: #fef08a; }
    .badge-connected { background: #166534; color: #bbf7d0; }
    .badge-ready { background: #1e40af; color: #bfdbfe; }
    .qr-frame {
      background: #ffffff;
      padding: 16px;
      border-radius: 16px;
      display: inline-block;
      margin-bottom: 20px;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
    }
    .qr-frame img {
      display: block;
      width: 260px;
      height: 260px;
    }
    .steps {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 18px;
      text-align: left;
      font-size: 13px;
      color: #cbd5e1;
      line-height: 1.6;
    }
    .steps ol {
      padding-left: 20px;
    }
    .steps li { margin-bottom: 6px; }
    .success-box {
      background: #064e3b;
      border: 1px solid #059669;
      border-radius: 12px;
      padding: 24px;
      color: #a7f3d0;
      font-size: 15px;
    }
    .success-icon { font-size: 48px; margin-bottom: 12px; }
  </style>
</head>
<body>
  <div class="card" id="app">
    <h1>Viditex Distribuidora</h1>
    <p class="sub">Automação de WhatsApp, Cotações e Despacho de Pedidos</p>

    <div id="content">Carregando status...</div>
  </div>

  <script>
    async function updateStatus() {
      try {
        const res = await fetch('/qr-data');
        const data = await res.json();
        const content = document.getElementById('content');

        if (data.status === 'connected') {
          content.innerHTML = \`
            <div class="success-box">
              <div class="success-icon">✅</div>
              <h2 style="color: #6ee7b7; margin-bottom: 8px;">WhatsApp Conectado!</h2>
              <p style="color: #d1fae5; font-size: 14px;">Seu WhatsApp está autenticado e pronto para receber cotações do Mercado Livre e despachar pedidos para o fornecedor.</p>
              <p style="margin-top: 12px; font-size: 12px; opacity: 0.8;">Conta: \${data.user ? data.user.id : 'Ativa'}</p>
            </div>
          \`;
        } else if (data.status === 'qr_ready' && data.qrImage) {
          content.innerHTML = \`
            <div class="badge badge-ready">Aguardando Leitura do QR Code</div>
            <div class="qr-frame">
              <img src="\${data.qrImage}" alt="QR Code WhatsApp" />
            </div>
            <div class="steps">
              <strong>Como conectar:</strong>
              <ol>
                <li>Abra o WhatsApp no seu smartphone</li>
                <li>Toque em <strong>Configurações</strong> ou <strong>Menu ⋮</strong></li>
                <li>Selecione <strong>Aparelhos Conectados</strong></li>
                <li>Toque em <strong>Conectar um Aparelho</strong> e aponte para este QR code</li>
              </ol>
            </div>
          \`;
        } else {
          content.innerHTML = \`
            <div class="badge badge-connecting">Inicializando Conexão WhatsApp...</div>
            <p style="color: #94a3b8; font-size: 14px; margin-top: 20px;">Aguarde alguns segundos enquanto o serviço prepara o QR Code.</p>
          \`;
        }
      } catch (err) {
        console.error(err);
      }
    }

    setInterval(updateStatus, 3000);
    updateStatus();
  </script>
</body>
</html>
    `);
});

// Endpoint compatível com Evolution API: Envio de Texto
// POST /message/sendText/:instance
app.post('/message/sendText/:instance', async (req, res) => {
    try {
        const { number, text } = req.body;
        if (!number || !text) {
            return res.status(400).json({ error: 'Parâmetros "number" e "text" são obrigatórios' });
        }
        if (!sock || connectionStatus !== 'connected') {
            return res.status(503).json({ error: 'WhatsApp desconectado. Escaneie o QR Code em /qrcode' });
        }

        const jid = formatJid(number);
        console.log(`[WhatsApp Outbound] Enviando texto para ${jid}: "${text.substring(0, 60)}..."`);
        const result = await sock.sendMessage(jid, { text });

        return res.json({
            status: 'success',
            key: result?.key,
            message: 'Mensagem enviada com sucesso'
        });
    } catch (err) {
        console.error('[WhatsApp Outbound] Erro ao enviar texto:', err.message);
        return res.status(500).json({ error: err.message });
    }
});

// Endpoint compatível com Evolution API: Envio de Mídia / PDF
// POST /message/sendMedia/:instance
app.post('/message/sendMedia/:instance', async (req, res) => {
    try {
        const { number, mediaMessage } = req.body;
        if (!number || !mediaMessage) {
            return res.status(400).json({ error: 'Parâmetros "number" e "mediaMessage" são obrigatórios' });
        }
        if (!sock || connectionStatus !== 'connected') {
            return res.status(503).json({ error: 'WhatsApp desconectado. Escaneie o QR Code em /qrcode' });
        }

        const jid = formatJid(number);
        const mediaUrl = mediaMessage.media;
        const caption = mediaMessage.caption || '';
        const mediatype = mediaMessage.mediatype || 'document';

        console.log(`[WhatsApp Outbound] Baixando mídia para envio para ${jid} de: ${mediaUrl}`);

        const response = await axios.get(mediaUrl, {
            responseType: 'arraybuffer',
            timeout: 30000
        });

        const buffer = Buffer.from(response.data);
        const contentType = response.headers['content-type'] || 'application/pdf';

        let msgOptions;
        if (mediatype === 'image') {
            msgOptions = {
                image: buffer,
                caption: caption
            };
        } else {
            msgOptions = {
                document: buffer,
                mimetype: contentType,
                fileName: 'etiqueta_envio.pdf',
                caption: caption
            };
        }

        const result = await sock.sendMessage(jid, msgOptions);
        console.log(`[WhatsApp Outbound] Mídia enviada com sucesso para ${jid}`);

        return res.json({
            status: 'success',
            key: result?.key,
            message: 'Mídia enviada com sucesso'
        });
    } catch (err) {
        console.error('[WhatsApp Outbound] Erro ao enviar mídia:', err.message);
        return res.status(500).json({ error: err.message });
    }
});

app.listen(PORT, () => {
    console.log(`[WhatsApp Service] Rodando localmente na porta ${PORT}`);
    console.log(`[WhatsApp Service] Acesse http://localhost:${PORT}/qrcode no navegador para conectar.`);
    startWhatsApp();
});
