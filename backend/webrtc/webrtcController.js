class WebRTCController {
    constructor(io, sipController) {
        // Configuração do socket.io para comunicação com o frontend
        this.sipController = sipController;
        this.io = io;

        // Evento chamado quando um cliente se conecta
        this.io.on('connection', (socket) => {
            console.log('Novo cliente conectado:', socket.id);

            // Evento chamado quando o cliente solicita iniciar uma conexão WebRTC
            socket.on('webrtc:offer', (data) => {
                this.handleOffer(socket, data);
            });

            // Evento chamado quando o cliente envia uma resposta de oferta
            socket.on('webrtc:answer', (data) => {
                this.handleAnswer(socket, data);
            });

            // Evento chamado quando o cliente envia um ICE candidate
            socket.on('webrtc:candidate', (data) => {
                this.handleCandidate(socket, data);
            });
        });
    }

    handleMessage(socket, message) {
        // Lógica para processar mensagens do WebRTC
        socket.emit('webrtc:message', { message });
    }

    // Método para lidar com a oferta de conexão WebRTC
    handleOffer(socket, offer) {
        // Lógica para processar a oferta e enviar para o destino correto
        console.log('Oferta recebida:', offer);

        // Encaminha a oferta para o SIPController para lidar com a sinalização SIP
        this.sipController.handleCall(socket, offer);
    }

    // Método para lidar com a resposta de oferta de conexão WebRTC
    handleAnswer(socket, answer) {
        // Lógica para processar a resposta de oferta e enviar de volta para o solicitante
        console.log('Resposta de oferta recebida:', answer);

        // Aqui você pode encaminhar a resposta para o outro peer no WebRTC
        socket.broadcast.emit('webrtc:answer', answer);
    }

    // Método para lidar com o ICE candidate enviado pelo cliente
    handleCandidate(socket, candidate) {
        // Lógica para processar o ICE candidate e enviar para o destino correto
        console.log('ICE candidate recebido:', candidate);

        // Aqui você pode encaminhar o candidato ICE para o outro peer no WebRTC
        socket.broadcast.emit('webrtc:candidate', candidate);
    }
}
  
module.exports = { WebRTCController };
  