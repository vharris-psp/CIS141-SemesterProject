from netmiko import ConnectHandler

def run_command(host, user, password, command):
    device = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': user,
        'password': password,
    }
    try: 
        connection = ConnectHandler(**device)
        output = connection.send_command(command)
        connection.disconnect()
        return output
    except Exception as e:
        return f"An error occurred: {e}"
        
        