import paramiko
from datetime import datetime

# =======================
# Configuration
# =======================
SSH_CONFIG = {
    "hostname": "192.168.100.125",
    "port": 22,
    "username": "codline_academy",
    "pkey_path": r"C:\Users\Muath\Desktop\TRA_Python\.ssh\id_rsa",
    "password": "mynameismuath"
}

DEVICES = [
    {"name": "router1"},
    {"name": "router2"},
    {"name": "router3"},
]


# =======================
# Security Checks
# =======================
def check_telnet(config: str) -> str:
    for line in config.lower().splitlines():
        if "transport input" in line and "telnet" in line:
            return "Telnet is enabled"
    return "Telnet is disabled"


def check_http_server(config: str) -> str:
    for line in config.lower().splitlines():
        if "ip http server" in line and "no ip http server" not in line:
            return "HTTP server is enabled"
    return "HTTP server is disabled"


def check_snmp(config: str) -> str:
    config = config.lower()
    if any(x in config for x in [
        "snmp-server community public",
        "snmp-server community private"
    ]):
        return "Default SNMP community strings found"
    return "No default SNMP community strings found"


# =======================
# SSH Connection
# =======================
def create_ssh_client(hostname, port, username, pkey_path, password):
    pkey = paramiko.RSAKey.from_private_key_file(pkey_path, password=password)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=hostname,
        port=port,
        username=username,
        pkey=pkey
    )

    return client


def fetch_running_config(client):
    """
    Execute 'show running-config' instead of reading a file
    """
    stdin, stdout, stderr = client.exec_command("show running-config")

    config = stdout.read().decode()
    error = stderr.read().decode().strip()

    if error:
        raise Exception(error)

    return config


def ssh_with_pkey(hostname, port, username, pkey_path):
    client = None
    try:
        client = create_ssh_client(
            hostname, port, username, pkey_path, SSH_CONFIG["password"]
        )

        print(f"Connected to {hostname}")

        return fetch_running_config(client)

    except Exception as e:
        raise Exception(f"SSH error on {hostname}: {e}")

    finally:
        if client:
            client.close()


# =======================
# Audit Logic
# =======================
def audit_device(device):
    result = {
        "name": device["name"],
        "telnet": "Audit failed",
        "http": "Audit failed",
        "snmp": "Audit failed",
        "error": None,
    }

    try:
        config = ssh_with_pkey(
            SSH_CONFIG["hostname"],
            SSH_CONFIG["port"],
            SSH_CONFIG["username"],
            SSH_CONFIG["pkey_path"]
        )

        result.update({
            "telnet": check_telnet(config),
            "http": check_http_server(config),
            "snmp": check_snmp(config)
        })

    except Exception as e:
        result["error"] = str(e)

    return result


# =======================
# Reporting
# =======================
def generate_report(results):
    filename = f"Audit_Report_{datetime.now():%Y-%m-%d}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("--- Network Device Audit Report ---\n\n")

        for r in results:
            file.write(f"Device: {r['name']}\n")

            if r["error"]:
                file.write(f"- Error: {r['error']}\n\n")
                continue

            file.write(f"- Telnet Status: {r['telnet']}\n")
            file.write(f"- HTTP Server Status: {r['http']}\n")
            file.write(f"- SNMP Status: {r['snmp']}\n\n")

    return filename


# =======================
# Main Execution
# =======================
def main():
    results = [audit_device(device) for device in DEVICES]

    report = generate_report(results)
    print(f"Audit report saved to {report}")


if __name__ == "__main__":
    main()
