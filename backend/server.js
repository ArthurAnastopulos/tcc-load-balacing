const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { WebRTCController } = require('./webrtc/webrtcController');
const { SIPController } = require('./sip/sipController');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const sipController = new SIPController();
const webRTCController = new WebRTCController(io, sipController);


// Configuração do cache de proxy
//app.use(express.static('public', { maxAge: 86400000 })); // Cache por 1 dia

// Manipuladores de eventos para WebRTC e SIP
io.on('connection', (socket) => {
    console.log('Novo cliente conectado');

    socket.on('disconnect', () => {
        console.log('Cliente desconectado');
    });

    // Manipuladores de eventos para WebRTC
    socket.on('webrtc:message', (message) => {
        webRTCController.handleMessage(socket, message);
    });

    // Manipuladores de eventos para SIP
    socket.on('sip:call', (data) => {
        sipController.handleCall(socket, data);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Servidor HTTP rodando na porta ${PORT}`);
});
