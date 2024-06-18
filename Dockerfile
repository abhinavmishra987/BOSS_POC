# Use a base image with Samba and Webmin
FROM debian:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    samba \
    smbclient \
    krb5-user \
    dnsutils \
    wget \
    gnupg \
    apt-transport-https \
    iproute2 \
    net-tools \
    perl \
    liblist-moreutils-perl \
    && apt-get clean

# Install Webmin
RUN wget -qO - http://www.webmin.com/jcameron-key.asc | apt-key add - \
    && echo "deb http://download.webmin.com/download/repository sarge contrib" > /etc/apt/sources.list.d/webmin.list \
    && apt-get update \
    && apt-get install -y webmin

# Expose necessary ports
EXPOSE 53/udp 53/tcp 88/udp 88/tcp 135/tcp 137/udp 138/udp 139/tcp 389/tcp 389/udp 445/tcp 464/tcp 464/udp 636/tcp 3268/tcp 3269/tcp 10000/tcp

# Add the script to set the Webmin root password and handle PID files
COPY set-webmin-password.sh /usr/local/bin/set-webmin-password.sh
RUN chmod +x /usr/local/bin/set-webmin-password.sh

# Run Samba and Webmin in the foreground
CMD ["sh", "-c", "/usr/local/bin/set-webmin-password.sh && smbd && nmbd && tail -f /var/log/samba/log.smbd"]
