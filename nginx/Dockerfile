# Use a Debian base image
FROM debian:buster-slim

# Update repositories and install Nginx and Certbot
RUN apt-get update && \
    apt-get install -y nginx certbot python-certbot-nginx cron && \
    apt-get clean

# Copy the custom Nginx configuration file to the Nginx configuration directory
COPY nginx.conf /etc/nginx/nginx.conf

# Expose HTTP and HTTPS ports
EXPOSE 80
EXPOSE 443

# Add a script to automatically renew SSL certificates
COPY certbot_renew.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/certbot_renew.sh
RUN crontab -l | { cat; echo "0 0 * * * /usr/local/bin/certbot_renew.sh"; } | crontab -

# Start a shell for interactive use
CMD ["/bin/bash"]