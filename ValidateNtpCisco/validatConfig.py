import re,sys
import mysql.connector
from netmiko import ConnectHandler
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract


def doValidation(DevicesInfos):

    pattern ="(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    ip_ntp = "20.20.20.20"
    
    for Devices in DevicesInfos:

         mydevice = {
            'host': Devices[0],
            "device_type": "cisco_ios",
            "username": "cisco",
            "password": "cisco",
            "secret":   "cisco123",
    }    
    
    #while True:

         net_connect = ConnectHandler(**mydevice)
         net_connect.enable()
         configuration = net_connect.send_command("show runn  | sect ntp ")
         #matches =re.finditer(pattern ,configuration)
         
         if(re.search(ip_ntp,configuration)):
              print("ntp valido")
         else:
               print("ntp invalido")
               net_connect.send_config_set("ntp server 20.20.20.20")

      
         

         
   



#Read the database

db = mysql.connector.connect(
host="localhost",
user="root",
passwd="Junior14@",
database="altice"
)
mycursor = db.cursor()
mycursor.execute("SELECT ip_de_gestao,hotspot  FROM Clientes_Altice_Simplificado")
myresult=mycursor.fetchall()

doValidation(myresult)





