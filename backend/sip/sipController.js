const JsSIP = require('jssip');

class SIPController {
    constructor() {
        // Configuração do JsSIP
        const configuration = {
            uri: 'sip:seu-usuario@seu-dominio.com',
            password: 'sua-senha',
            sockets: [new JsSIP.WebSocketInterface('wss://seu-dominio.com:8089/ws')],
        };
      
        // Criação da instância do JsSIP UA (User Agent)
        this.ua = new JsSIP.UA(configuration);
      
        // Evento chamado quando a conexão WebSocket é aberta
        this.ua.on('connected', () => {
            console.log('Conexão WebSocket estabelecida');
        });
    
        // Evento chamado quando a conexão WebSocket é fechada
        this.ua.on('disconnected', () => {
            console.log('Conexão WebSocket desconectada');
        });
    
        // Evento chamado quando uma chamada é recebida
        this.ua.on('newRTCSession', (e) => {
            console.log('Nova chamada recebida:', e);
            this.handleIncomingCall(e); // Chama método para manipular chamada recebida
        });
    }

    // Método para manipular chamada recebida
    handleIncomingCall(session) {
        // Lógica para manipular a chamada recebida
        const callInfo = {
            from: session.remote_identity.display_name,
            uri: session.remote_identity.uri.toString(),
            state: session.connection_state,
        };

        // Envia informações da chamada de volta para o frontend
        this.emitToSocket('sip:incomingCall', callInfo);
    }

    // Método para iniciar uma chamada SIP
    handleCall(socket, data) {
        // Lógica para iniciar uma chamada SIP
        const callOptions = {
            // Opções para a chamada SIP
        };

        // Inicia a chamada usando JsSIP
        const session = this.ua.call('sip:destino@dominio.com', callOptions);

        // Adiciona manipuladores de eventos à sessão
        session.on('accepted', () => {
            console.log('Chamada aceita');
        });
    
        session.on('failed', () => {
            console.log('Chamada falhou');
        });
    
        session.on('ended', () => {
            console.log('Chamada encerrada');
        });

        // Emitir evento para o socket, se necessário
        this.emitToSocket('sip:call', { data });

        // Retorna a sessão para que possa ser utilizada por outros métodos
        return session;
    }

    handleAnswer(socket, callId, session) {
        // Lógica para responder a uma chamada SIP
        session.answer();
        socket.emit('sip:answer', { callId });
    }

    handleTerminate(socket, callId, session) {
        // Lógica para terminar uma chamada SIP
        session.terminate();
        socket.emit('sip:terminate', { callId });
    }

    // Método para emitir evento para o socket
    emitToSocket(eventName, data) {
        // Emitir evento para o socket, se necessário
        io.emit(eventName, data);
    }
}
  
module.exports = { SIPController };
  