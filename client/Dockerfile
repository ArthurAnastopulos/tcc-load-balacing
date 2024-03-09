# Imagem base desejada para o frontend
FROM node:latest

# Diretório de trabalho dentro do contêiner
WORKDIR /app/frontend

# Copia os arquivos do frontend para o contêiner
COPY . .

# Instala as dependências do frontend
RUN npm install

# Comando de construção do frontend (build)
CMD ["npm", "run", "build"]
