const https = require('https');
const fs = require('fs');
const path = require('path');

const options = {
  key: fs.readFileSync('./chave-privada.pem'),
  cert: fs.readFileSync('./certificado.pem')
};

https.createServer(options, (req, res) => {
  let filePath = '.' + req.url;
  if (filePath === './') {
    filePath = './index.html';
  }

  const extname = path.extname(filePath);
  let contentType = 'text/html';
  switch (extname) {
    case '.js':
      contentType = 'text/javascript';
      break;
  }

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404);
        res.end('404 Not Found');
      } else {
        res.writeHead(500);
        res.end('500 Internal Server Error');
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
}).listen(443, () => {
  console.log('Servidor HTTPS iniciado na porta 443');
});
