# Use a Debian base image
FROM debian:buster-slim

# Update repositories and install Nginx and Certbot
RUN apt-get update && \
    apt-get install -y nginx certbot python3-certbot-nginx libnginx-mod-stream libnginx-mod-http-geoip libnginx-mod-rtmp && \
    apt-get clean

# Expose HTTP and HTTPS ports
EXPOSE 80/tcp
EXPOSE 443/tcp

# Add a script to automatically renew SSL certificates
COPY certbot_renew.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/certbot_renew.sh

# Start a shell for interactive use
CMD ["/bin/bash"]
