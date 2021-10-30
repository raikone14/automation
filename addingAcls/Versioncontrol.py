import mysql.connector
from netmiko import ConnectHandler
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from napalm import get_network_driver
import json


def doValidation(DevicesInfos):

    for Devices in DevicesInfos:

        driver=get_network_driver("ios")
        device = driver(hostname=Devices[0],
                 username="junior",
                 password="cisco",
)
        print("acessing device....." + Devices[0]) 
        device.open()
        get_facts = device.get_facts()
        print(get_facts)
        device.load_merge_candidate(filename="ACL.cfg")
        device.commit_config()
        device.close()




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