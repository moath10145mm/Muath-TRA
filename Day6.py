from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
from datetime import datetime

# List of network devices
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.1",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.2",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "cisco_ios",
        "ip": "10.0.0.1",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "juniper_junos",
        "ip": "192.168.1.3",
        "username": "admin",
        "password": "password"
    }
]

# Directory to store backups
backup_dir = "./backups"
os.makedirs(backup_dir, exist_ok=True)

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Loop through each device
for device in devices:
    ip = device.get("ip")
    device_type = device.get("device_type")
    net_connect = None

    print(f"\nAttempting to connect to {ip} ({device_type})...")

    try:
        # Connect to the device
        net_connect = ConnectHandler(**device)
        print(f"Successfully connected to {ip}.")

        # Get hostname
        if device_type.startswith("cisco"):
            hostname = net_connect.find_prompt().strip("#>")  # Removes trailing # or >
        elif device_type.startswith("juniper"):
            hostname = net_connect.find_prompt().strip(">")  # Juniper prompts end with >
        else:
            hostname = ip  # Fallback to IP if unknown device type

        print(f"Device Hostname: {hostname}")
        print(f"Retrieving running configuration from {hostname}...")

        # Retrieve running configuration
        if device_type.startswith("cisco"):
            running_config = net_connect.send_command("show running-config")
        elif device_type.startswith("juniper"):
            running_config = net_connect.send_command("show configuration")
        else:
            running_config = net_connect.send_command("show running-config")  # Default command

        # Construct backup filename
        backup_file = f"{hostname}_{current_date}.txt"
        backup_path = os.path.join(backup_dir, backup_file)

        # Write config to file
        with open(backup_path, "w") as f:
            f.write(running_config)

        print(f"Configuration backup for {hostname} saved to {backup_path} successfully.")

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Error backing up configuration for {ip}: {e}")

    finally:
        if net_connect:
            net_connect.disconnect()
            print(f"Disconnected from {ip}.")
