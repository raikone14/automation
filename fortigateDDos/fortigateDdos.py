from netmiko.fortinet import FortinetSSH
from netmiko import ConnectHandler

fortigate = {
    'device_type' : 'fortinet',
    'host' : '10.5.59.41',
    'username' : 'admin2',
    'password' : 'password',
    'port' : 22,
}

net_connect = ConnectHandler(**fortigate)


config_file = "ddos.txt"
output = net_connect.send_config_from_file(config_file)
    


#output = net_connect.send_command("show")
#print(output)
net_connect.disconnect()
