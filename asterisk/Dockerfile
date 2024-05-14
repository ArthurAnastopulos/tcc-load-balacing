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

# Criar diretório para as chaves do Asterisk
# 808RUN mkdir -p /etc/asterisk/keys/

# Copie seus certificados DTLS para o diretório padrão do Asterisk
# COPY ./asterisk-conf/asterisk.crt /etc/asterisk/keys/asterisk.crt
# COPY ./asterisk-conf/asterisk.key /etc/asterisk/keys/asterisk.key

# Definir permissões e propriedades adequadas para os arquivos
# RUN chmod 600 /etc/asterisk/keys/asterisk.crt /etc/asterisk/keys/asterisk.key \
    # && chown asterisk:asterisk /etc/asterisk/keys/asterisk.crt /etc/asterisk/keys/asterisk.key

# # Configurar o caminho para o OpenSSL no script ast_tls_cert
# RUN sed -i 's|OPENSSL=openssl|OPENSSL=/usr/bin/openssl|g' /usr/local/src/asterisk*/contrib/scripts/ast_tls_cert

# #Gerar certificado TLS para o Asterisk
# RUN /usr/local/src/asterisk*/contrib/scripts/ast_tls_cert -C $SERVER_IP -O "My Cool App" -d /etc/asterisk/keys/

# Defina as permissões adequadas para o diretório do banco de dados do Asterisk
RUN chown -R asterisk:asterisk /var/lib/asterisk
RUN chown -R asterisk:asterisk /var/log

# Copiar arquivos de configuração personalizados
COPY ./asterisk-conf/http.conf /etc/asterisk/http.conf
COPY ./asterisk-conf/extensions.conf /etc/asterisk/extensions.conf
# COPY ./asterisk-conf/rtp.conf /etc/asterisk/rtp.conf
# COPY ./asterisk-conf/pjsip.conf /etc/asterisk/sip.conf
COPY ./asterisk-conf/pjsip.conf /etc/asterisk/pjsip.conf

# Expor a porta do Asterisk (mude para a porta do Asterisk, se necessário)
EXPOSE 5060/udp
EXPOSE 5060/tcp
EXPOSE 5061/tcp
EXPOSE 8080/tcp

# Comando padrão para iniciar o Asterisk
CMD ["/usr/sbin/asterisk", "-vvvdddf", "-T", "-W", "-U", "asterisk", "-p"]
