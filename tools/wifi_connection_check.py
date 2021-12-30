import os
import platform
import getpass
# from core import *
# import pyping
import subprocess
import time

def createNewConnection(name, SSID, key):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+key+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    if platform.system() == "Windows":
        command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
        with open(name+".xml", 'w') as file:
            file.write(config)
    elif platform.system() == "Linux":
        command = "nmcli dev wifi connect '"+SSID+"' password '"+key+"'"
    elif platform.system() == "Darwin":
        command = "networksetup -setairportnetwork en0" + " " + SSID + " " + key
    os.system(command)
    if platform.system() == "Windows":
        os.remove(name+".xml")

def connect(name, SSID):
    if platform.system() == "Windows":
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli con up "+SSID
    elif platform.system() == "Darwin":
        for ping in range(1, 10):
            address = "google.com"
            res = subprocess.call(['ping', '-c', '3', address])
            if res == 0:
                print("ping to", address, "OK")
            elif res == 2:
                print("no response from", address)
            else:
                print("ping to", address, "failed!")

    # os.system(command)

def displayAvailableNetworks():
    print(platform.system())
    if platform.system() == "Windows":
        command = "netsh wlan show networks interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli dev wifi list"
    elif platform.system() == "Darwin":
        command = "networksetup -listpreferredwirelessnetworks en0"
    os.system(command)


try:
    displayAvailableNetworks()
    option = input("New connection (y/N)? ")
    if option == "N" or option == "":
        name = input("Name: ")
        connect(name, name)
        print("If you aren't connected to this network, try connecting with correct credentials")
    elif option == "y":
        name = input("Name: ")
        key = getpass.getpass("Password: ")
        createNewConnection(name, name, key)
        time.sleep(10)
        connect(name, name)
        print("If you aren't connected to this network, try connecting with correct credentials")
except KeyboardInterrupt as e:
    print("\nExiting...")