FROM opensips/opensips

# Adicione quaisquer personalizações ou configurações necessárias aqui

# Copie os arquivos de configuração para o diretório correto no contêiner
COPY opensips.cfg /usr/local/etc/opensips/opensips.cfg

# Exponha as portas necessárias para o OpenSIPS
EXPOSE 5060/udp
EXPOSE 5060/tcp

# Comando padrão para iniciar o OpenSIPS
CMD ["opensips", "-F"]
