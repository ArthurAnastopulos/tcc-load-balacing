document.addEventListener('DOMContentLoaded', function() {
    // SIP Configuration
    const configuration = {
        uri: 'sip:1060@192.168.1.100',
        password: '1234',
        sockets: [new JsSIP.WebSocketInterface('wss://192.168.1.100:8089')],
        register: true
    };

    // Create JsSIP User Agent
    const userAgent = new JsSIP.UA(configuration);

    // Register event handlers
    userAgent.on('registered', () => {
        console.log('Registered with SIP server');
    });

    userAgent.on('unregistered', () => {
        console.log('Unregistered from SIP server');
    });

    // Handle incoming calls
    userAgent.on('newRTCSession', (e) => {
        const session = e.session;
        console.log('Incoming call received');
        
        // Handle incoming call answer
        session.on('accepted', () => {
            console.log('Call accepted');
            const audioElement = document.getElementById('remoteAudio');
            audioElement.srcObject = session.connection.getRemoteStreams()[0];
        });
    });

    // Handle Call Button Click
    document.getElementById('callBtn').addEventListener('click', async () => {
        const options = {
            mediaConstraints: { audio: true, video: false }
        };

        // Make outgoing call
        const session = userAgent.call('sip:1061@192.168.1.100', options);
        console.log('Outgoing call initiated');
        
        // Handle outgoing call answer
        session.on('confirmed', () => {
            console.log('Call confirmed');
        });
    });

    // Handle Hangup Button Click
    document.getElementById('hangupBtn').addEventListener('click', () => {
        userAgent.terminateSessions();
        console.log('Call terminated');
    });

    // Start JsSIP User Agent
    userAgent.start();
});
