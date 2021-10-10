import mysql.connector
from netmiko import ConnectHandler
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract



#Fuction to do the backups of the devices

def doBackup(DevicesInfos):
    
    
    #print(type(mydevice))
    
    for Devices in DevicesInfos:

        mydevice = {
            'host': Devices[0],
            "device_type": "cisco_ios",
            "username": "cisco",
            "password": "cisco",
            "secret":   "cisco123",
    } 
        #print(type(mydevice.get("host")))
        net_connect = ConnectHandler(**mydevice)
        net_connect.enable()
        #pront=(net_connect.find_prompt())
        configuration = net_connect.send_command("show runn")
        #print(configuration)
        file = open(Devices[1] + "_output.txt", "w")
        print("Creating the bacukp" + Devices[1])
        file.write(configuration)
        file.close()
        net_connect.disconnect()



#Read the database

db = mysql.connector.connect(
host="localhost",
user="root",
passwd="password",
database="altice"
)
mycursor = db.cursor()
mycursor.execute("SELECT ip_de_gestao,hotspot  FROM Clientes_Altice_Simplificado")
myresult=mycursor.fetchall()


doBackup(myresult)

