#!/bin/bash                                                                     

# Set Webmin root password                                                      
/usr/share/webmin/changepass.pl /etc/webmin root password

# Check if Webmin is running and remove the PID file if necessary               
if [ -f /var/webmin/miniserv.pid ]; then
  PID=$(cat /var/webmin/miniserv.pid)
  if [ -e /proc/$PID ]; then
    echo "Webmin is already running with PID $PID"
  else
    echo "Removing stale PID file"
    rm -f /var/webmin/miniserv.pid
    service webmin start
  fi
else
  service webmin start
fi

