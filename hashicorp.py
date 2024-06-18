import os
import hvac

# Set the Vault address
vault_addr = os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200')
# export VAULT_TOKEN="hvs.U14PnzKTWM84vntU5M6OsIIv"
vault_token = os.getenv('VAULT_TOKEN', 'hvs.U14PnzKTWM84vntU5M6OsIIv')
# Initialize the client
client = hvac.Client(url=vault_addr)

# Authenticate to Vault
# Replace 'root' with your root token from the Vault dev server output
client.token = vault_token

# Check if the client is authenticated
if client.is_authenticated():
    print("Successfully authenticated to Vault")
else:
    print("Failed to authenticate to Vault")

# Write a secret to Vault
write_response = client.secrets.kv.v2.create_or_update_secret(
    path='mysecret',
    secret=dict(password='mySuperSecretPassword')
)
print(f"Secret written to Vault: {write_response}")

# Read the secret from Vault
read_response = client.secrets.kv.v2.read_secret_version(path='mysecret')
print(f"Secret read from Vault: {read_response['data']['data']}")

# Delete the secret from Vault
delete_response = client.secrets.kv.v2.delete_metadata_and_all_versions(path='mysecret')
print(f"Secret deleted from Vault: {delete_response}")
