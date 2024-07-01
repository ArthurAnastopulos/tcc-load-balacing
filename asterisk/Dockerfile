# Use a imagem Debian Slim como base
FROM debian:buster-slim

# Define argument for IP address
ARG SERVER_IP

# Configurar os módulos desejados
ENV ASTERISK_MODULES="chan_sip res_srtp res_pjsip res_pjsip_session res_pjsip_registrar res_pjsip_transport_websocket cdr_sqlite3_custom cel_sqlite3_custom pbx_spool"

# Atualizar o repositório e instalar pacotes necessários
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl tar wget gcc g++ ncurses-dev libxml2-dev libsqlite3-dev sqlite3 \
    uuid-dev libssl-dev libjansson-dev build-essential libedit-dev openssl \
    libsrtp2-dev libopus-dev && \
    rm -rf /var/lib/apt/lists/*

RUN cd /tmp &&\
    wget --no-check-certificate https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/2.14/pjproject-2.14.tar.bz2

# Baixar e compilar o Asterisk
RUN curl -o asterisk.tar.gz \
    http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-18-current.tar.gz && \
    tar zxfv asterisk.tar.gz && \
    cd asterisk* && \
    ./configure --with-pjproject-bundled PJPROJECT_URL=/tmp/pjproject-2.14.tar.bz2 && \
    make && \
    make install && \
    make config && \
    make samples

# Executar o make menuselect para selecionar os módulos desejados
RUN cd asterisk* && \
    make menuselect.makeopts && \
    menuselect/menuselect --enable $ASTERISK_MODULES && \
    make && \
    make install

# Adicionar o usuário "asterisk"
RUN useradd -ms /bin/bash asterisk

# Remover o arquivo de configuração padrão do Asterisk
RUN rm /etc/asterisk/sip.conf

# Defina as permissões adequadas para o diretório do banco de dados do Asterisk
RUN chown -R asterisk:asterisk /var/lib/asterisk
RUN chown -R asterisk:asterisk /var/log

# Expor a porta do Asterisk (mude para a porta do Asterisk, se necessário)
EXPOSE 5060

# Comando padrão para iniciar o Asterisk
CMD ["/usr/sbin/asterisk", "-vvvdddf", "-T", "-W", "-U", "asterisk", "-p"]
