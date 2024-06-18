#!/bin/bash

set -e

# Function to start a service and check its status
start_service() {
    service_name=$1
    echo "Starting ${service_name}..."
    service ${service_name} start || true
    service ${service_name} status || true
}

# Start Samba services
start_service smbd
start_service nmbd

# Start Webmin
start_service webmin

# Keep the container running
echo "All services started. Keeping the container running..."
tail -f /var/log/samba/log.smbd
