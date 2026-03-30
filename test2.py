IPv4 = input("Enter the IPv4 Please: ")
Check_Ip = IPv4.split('.')

for part in Check_Ip:

 print (part)















# def is_valid_ipv4(ip_str):
#     # Rule 1: Must contain exactly four octets separated by periods 
#     octets = ip_str.split('.')
#     if len(octets) != 4:
#         return False
    
#     for octet in octets:
#         # Rule 2: Each octet must consist only of digits 
#         if not octet.isdigit():
#             return False
        
#         # Rule 3: Each octet must be between 0 and 255 
#         if not (0 <= int(octet) <= 255):
#             return False
            
#     return True

# # Main Execution
# user_input = input("Enter an IPv4 address to validate: ") # [cite: 5]

# if is_valid_ipv4(user_input):
#     print(f"Success: '{user_input}' is a valid IPv4 address.") # [cite: 8]
# else:
#     print(f"Error: '{user_input}' is an invalid IPv4 address.") # [cite: 8]