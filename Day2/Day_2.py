from Day1.Day_1 import is_valid_ipv4
import ipaddress

IPv4 = input("Enter the IPv4 Please: ")

if not is_valid_ipv4(IPv4):
    print("Invalid IP address.")
    exit()

cidr_input = input("Enter CIDR: ")


try:
    cidr = int(cidr_input)
    if cidr < 0 or cidr > 32:
        raise ValueError
except ValueError:
    print("Invalid CIDR.")
    exit()

network = ipaddress.IPv4Network(f"{IPv4}/{cidr}", strict=False)

print("Network Address:", network.network_address)
print("Broadcast Address:", network.broadcast_address)
