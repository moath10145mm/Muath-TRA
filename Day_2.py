from Day_1 import is_valid_ipv4
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
print(network.hosts)


#--------------------------------------------------------------------------------------------------------------
# def subnet_calculator(ip, cidr):
#     try:
#         # Validate CIDR
#         if not isinstance(cidr, int):
#             raise ValueError("CIDR must be a number.")
#         if cidr < 0 or cidr > 32:
#             raise ValueError("CIDR must be between 0 and 32.")

#         # Create network object
#         network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)

#         network_address = network.network_address
#         broadcast_address = network.broadcast_address

#         # Calculate usable hosts
#         if cidr == 32:
#             usable_hosts = 1
#         elif cidr == 31:
#             usable_hosts = 2
#         else:
#             usable_hosts = network.num_addresses - 2

#         print(f"Network Address: {network_address}")
#         print(f"Broadcast Address: {broadcast_address}")
#         print(f"Usable Hosts: {usable_hosts}")

#     except ValueError as e:
#         print(f"Error: {e}")
#     except ipaddress.AddressValueError:
#         print("Error: Invalid IPv4 address format.")

# # ---- CLI Input ----
# try:
#     ip_input = input("Enter IPv4 address: ")
#     cidr_input = input("Enter CIDR prefix: ")

#     # Convert CIDR to int safely
#     cidr_input = int(cidr_input)

#     subnet_calculator(ip_input, cidr_input)

# except ValueError:
#     print("Error: CIDR must be a numeric value.")
