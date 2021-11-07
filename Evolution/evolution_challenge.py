"""
Code to connect collect information from netbox "device ip,vendor, model etc"
and connect into the devices to collect sofware version,
and insert this sofware into netvbox
"""
from pprint import pprint
import pynetbox
from napalm import get_network_driver
import pytest



class NetworkDevice:
    """
    Class to hadle devices information
    """
    def __init__ (self,hostname,ip_address,vendor):
        self.hostname=hostname
        self.ip_address=ip_address
        self.vendor=vendor
        self.software_version=None


def populate_software(device_soft):
    """
    this function insert the sofware version into the custom field named Sofware Version
    """
    rtr = nb.dcim.devices.get(name=device_soft.hostname)
    rtr.custom_fields['Software Version'] = device_soft.software_version
    pprint("Inserting software version in:" + str(device_soft.hostname))
    rtr.save()
    #assert rtr.custom_fields['Software Version'] != " "
    return rtr.custom_fields['Software Version']


def test_software(value_to_be_tested):
    """
    this function test if sofware is not empity
    """
    print("testing if sofware is not empty")
    assert value_to_be_tested != " "

def create_connection(mydevices):
    """
    Fuction to connect into each device and get the sofware version,
    I asked to type the password for security reasons,
    but I also could define a default password
    """

    #drivers_types=["ios","junos","ros","asa","eos"]
    #Juniper,Cisco,Mikrotik,Arista

    for net_device in mydevices:
        driver_type=""
        password_dev=input("type the device password for device  "
                            + str( net_device.hostname)+ ": ")

        if net_device.vendor.upper() == "CISCO":
            driver_type="ios"
        elif net_device.vendor.upper() == "JUNIPER":
            driver_type="junos"
        elif net_device.vendor.upper() == "MIKROTIK":
            driver_type="ros"
        elif net_device.vendor.upper() == "ARISTA":
            driver_type="eos"
        else:
            print("DEVICE NOT FOUND")

        if driver_type != "":

            driver=get_network_driver(driver_type)
            device_temp = driver(hostname=net_device.ip_address,
                 username="admin",
                 password=password_dev,
)
            pprint("Collecting software version in:" + str(net_device.hostname))
            try:
                device_temp.open()
                net_device.software_version= device_temp.get_facts()['os_version']
            except:
                print("unable to connect into the device")
            finally:
                device_temp.close()
            #Call function populate
            test_software(net_device.software_version)
            populate_software(net_device)





nb = pynetbox.api(
url="http://localhost:8000",
token="0123456789abcdef0123456789abcdef01234567")


#Select devices that are active and part of tenant group Noc in this case id=1
devices = nb.dcim.devices.filter(status="active", tenant_group_id=1)

connected_devices=[]
for device in devices:
    hostname_dev=(device)
    #Remove the mask of the ip
    ip_address_dev=(device["primary_ip"]["address"]).split("/")[0]
    vendor_dev=(device["device_type"] ["manufacturer"] ["display"])
    new_device= NetworkDevice(hostname_dev,ip_address_dev,vendor_dev)
    connected_devices.append(new_device)
#Calls function to connect_into the devices
create_connection(connected_devices)
