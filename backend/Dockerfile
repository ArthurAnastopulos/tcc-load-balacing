# Imagem base desejada para o backend (por exemplo, Node.js)
FROM node:latest

# Diretório de trabalho dentro do contêiner
WORKDIR /app/backend

# Copia os arquivos do backend para o contêiner
COPY . .

# Instala as dependências do backend
RUN npm install

# Comando de inicialização do backend
CMD ["npm", "start"]
