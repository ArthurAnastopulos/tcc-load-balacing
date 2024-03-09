# Dockerfile para o PostgreSQL com configurações específicas

# Use uma imagem base do PostgreSQL
FROM postgres:latest

# Instale as bibliotecas necessárias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copie o script Python e os arquivos de inicialização SQL
COPY script_cache.py /docker-entrypoint-initdb.d/script_cache.py
COPY init-script.sql /docker-entrypoint-initdb.d/init-script.sql

# Defina variáveis de ambiente se necessário
ENV PYTHONPATH=/usr/local/lib/python3.8/dist-packages

# Comando padrão para iniciar o contêiner
CMD ["postgres"]
