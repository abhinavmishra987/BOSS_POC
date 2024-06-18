#!/bin/bash

LDAP_ADMIN_DN="cn=admin,dc=example,dc=com"
LDAP_ADMIN_PASSWORD="adminPassword123"
LDAP_BASE_DN="dc=example,dc=com"
NEW_USER_UID="jdoe"
NEW_USER_CN="John Doe"
NEW_USER_SN="Doe"
NEW_USER_PASSWORD="{SSHA}VpglP2I9Qq6O8/UuL9nHb7N+5CkzQh8e"
NEW_USER_SID="S-1-5-21-123456789-123456789-123456789-10001"
NEW_USER_NT_PASSWORD="E52CAC67419A9A224A3B108F3FA6CB6D"

# Create LDAP user
cat <<EOF | ldapadd -x -D "$LDAP_ADMIN_DN" -w "$LDAP_ADMIN_PASSWORD"
dn: uid=$NEW_USER_UID,ou=Users,$LDAP_BASE_DN
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: $NEW_USER_CN
sn: $NEW_USER_SN
uid: $NEW_USER_UID
uidNumber: 10001
gidNumber: 10000
homeDirectory: /home/$NEW_USER_UID
loginShell: /bin/bash
gecos: $NEW_USER_CN
userPassword: $NEW_USER_PASSWORD
EOF

# Add Samba attributes
cat <<EOF | ldapmodify -x -D "$LDAP_ADMIN_DN" -w "$LDAP_ADMIN_PASSWORD"
dn: uid=$NEW_USER_UID,ou=Users,$LDAP_BASE_DN
changetype: modify
add: objectClass
objectClass: sambaSamAccount
-
add: sambaSID
sambaSID: $NEW_USER_SID
-
add: sambaNTPassword
sambaNTPassword: $NEW_USER_NT_PASSWORD
-
add: sambaPwdLastSet
sambaPwdLastSet: 0
EOF

# Set Samba password
(echo "sambaPassword123"; echo "sambaPassword123") | smbpasswd -a -s $NEW_USER_UID

# Start Samba
exec "$@"
