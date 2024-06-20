#!/bin/bash

# Renovar os certificados SSL usando o Certbot
certbot renew
# Recarregar o Nginx para aplicar as alterações
nginx -s reload
