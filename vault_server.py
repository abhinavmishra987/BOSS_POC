import subprocess
import re
import time

def start_vault_server():
    # Start Vault server in development mode and capture the output
    process = subprocess.Popen(
        ['vault', 'server', '-dev'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # Read the output to capture the root token
    for line in process.stdout:
        print(line, end='')  # Optional: Print the output for debugging
        if "Root Token:" in line:
            root_token = line.split("Root Token:")[1].strip()
            return root_token

    # If the process ends, wait for it to properly close
    process.wait()

    return None

# Start the Vault server and fetch the root token
root_token = start_vault_server()
if root_token:
    print(f"Root Token: {root_token}")
else:
    print("Failed to retrieve the root token")
