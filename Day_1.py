def is_valid_ipv4(IPv4):
    
    Check_Ip = IPv4.split('.')

    if len(Check_Ip) != 4:

        return False
    
    for part in Check_Ip:
        if not part.isdigit():
            return False

        if not (0 <= int(part) <= 255):
            return False
            
            
    return True


IPv4 = input("Enter the IPv4 Please: ")
    
if is_valid_ipv4(IPv4):
     print(f"Success '{IPv4}' is a valid IPv4 address.")
else:
        print(f"Error '{IPv4}' is an invalid IPv4 address.")


