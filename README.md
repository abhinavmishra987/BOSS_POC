
sudo docker-compose up

sudo docker exec -it samba-ldap-webmin service webmin start


sudo docker run -it --entrypoint=/bin/bash samba-ldap-webmin


ldapsearch -x -H ldap://localhost -b "ou=users,dc=example,dc=com" -D "cn=admin,dc=example,dc=com" -W "(objectClass=inetOrgPerson)"



file version  in airflow  to find all the directory changes