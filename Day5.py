import paramiko
import os

# --- CONFIGURATION ---
hostname = "192.168.100.72"
username = "SSH Muath@192.168.100.72"
# Path to the private key you created in Step 1
private_key_path = os.path.expanduser("~/.ssh/id_rsa_paramiko")

def run_ssh_key_task():
    # 1. Verify the key file exists locally first
    if not os.path.exists(private_key_path):
        print(f"Error: Private key not found at {private_key_path}")
        return

    client = paramiko.SSHClient()
    
    # Auto-accept the remote server's host key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Attempting to connect to {hostname} via SSH Key...")
        
        # 2. Load the RSA Private Key
        # If you used a passphrase during generation, add: password='your_passphrase'
        key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # 3. Connect using pkey (Private Key) instead of a password
        client.connect(hostname=hostname, username=username, pkey=key)
        
        print("Successfully authenticated using SSH Key!")

        # 4. Run a command to verify the session
        stdin, stdout, stderr = client.exec_command("echo 'Connected as: ' $(whoami) && uptime")
        
        print("\n--- Command Result ---")
        print(stdout.read().decode())

    except paramiko.AuthenticationException:
        print("Authentication failed. Please verify the public key is in the remote 'authorized_keys' file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    run_ssh_key_task()