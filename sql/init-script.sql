-- Arquivo init-script.sql

-- Criação da tabela de usuários SIP
CREATE TABLE usuarios_sip (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    nome VARCHAR(100)
);

-- Criação da tabela de registros de chamadas SIP
CREATE TABLE registros_chamadas_sip (
    id SERIAL PRIMARY KEY,
    de_username VARCHAR(50) NOT NULL,
    para_username VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duracao INTEGER
);

-- Criação da tabela de usuários WebRTC
CREATE TABLE usuarios_webrtc (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    nome VARCHAR(100)
);

-- Criação da tabela de registros de chamadas WebRTC
CREATE TABLE registros_chamadas_webrtc (
    id SERIAL PRIMARY KEY,
    de_username VARCHAR(50) NOT NULL,
    para_username VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duracao INTEGER
);
