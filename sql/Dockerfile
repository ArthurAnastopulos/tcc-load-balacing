# Use Debian as base image
FROM debian:buster-slim

# Install MariaDB server
RUN apt-get update && \
    apt-get install -y gnupg2 wget unzip mariadb-server && \
    apt-get clean

# Initialize and start MariaDB
RUN mkdir -p /var/run/mysqld && \
    chown -R mysql:mysql /var/run/mysqld && \
    /etc/init.d/mysql start && \
    mysqladmin -u root password 'tccIfsc2024'

# Create OpenSIPS database and tables
RUN echo "CREATE DATABASE opensips;" | mysql -u root -p'tccIfsc2024' && \
    opensips-cli -x database create opensips && \
    mysql opensips -e "show tables"

# Create MySQL user and grant privileges
RUN mysql -u root -p'tccIfsc2024' -e "CREATE USER 'opensips'@'localhost' IDENTIFIED BY 'opensipsrw';" && \
    mysql -u root -p'tccIfsc2024' -e "GRANT ALL PRIVILEGES ON opensips.* TO 'opensips'@'localhost';" && \
    mysql -u root -p'tccIfsc2024' -e "FLUSH PRIVILEGES"
