import threading
from tkinter import filedialog
import time
import platform
import subprocess
import server as ota
import cell_on_off_control as cell_on_off
import sys, os
import socket


def check_wifi_ssid_ip_setting():
    try:
        print(platform.system())
        if platform.system() == "Windows":
            process = subprocess.Popen(
                ['Netsh', 'WLAN', 'show', "interfaces"],
                stdout=subprocess.PIPE)
            out, err = process.communicate()
            process.wait()
            print(out)
            if "OHCOACH" in str(out):
                print("SSID OK")
            else:
                print("Connect to right WiFi -> OHCOACHxxxx")
                raise Exception("Connect to right WiFi -> OHCOACHxxxx")

            process2 = subprocess.Popen(['ipconfig'], stdout=subprocess.PIPE)
            out2, err2 = process2.communicate()
            process2.wait()
            print(out2)

            if "192.168.1.254" in str(out2):
                print("IP set to 192.168.1.254")
            else:
                print("Check your ip setting")
                raise Exception("Check your ip setting")

        elif platform.system() == "Darwin":
            process = subprocess.Popen(
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
                stdout=subprocess.PIPE)
            out, err = process.communicate()
            process.wait()
            print(out)
            if "OHCOACH" in str(out):
                print("SSID OK")
            else:
                print("Connect to right WiFi -> OHCOACHxxxx")
                raise Exception("Connect to right WiFi -> OHCOACHxxxx")

            process2 = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
            out2, err2 = process2.communicate()
            process2.wait()
            print(out2)

            if "192.168.1.254" in str(out2):
                print("IP set to 192.168.1.254")
            else:
                print("Check your ip setting")
                raise Exception("Check your ip setting")

    except:
        print("Error happened close window after 10secs")
        time.sleep(10)
        exit()


def cell_entered_ota():
    for i in range(1, 37):
        cell_ctr = cell_on_off.Scanning()
        print("Start cell %d OTA update !" % i)
        cell_port = cell_ctr.main(i)
        print(cell_port)
        time.sleep(30)
        # print("cell number / ota flag = ", i, ota.OTA_flag)

        if ota.OTA_flag == 1:
            print("Cell number %d update SUCCESS !" % i)
        else:
            print("Cell number %d update FAIL !" % i)

        ota.save_ota_done(0)


# TODO:
if __name__ == '__main__':
    check_wifi_ssid_ip_setting()

    if getattr(sys, 'frozen', False):
        program_directory = os.path.dirname(os.path.abspath(sys.executable))
    else:
        program_directory = os.path.dirname(os.path.abspath(__file__))
    # path = filedialog.askdirectory()
    path = program_directory
    print(path)
    ota_thread = threading.Thread(target=ota.ota_server_open, args=[path])

    ota_thread.start()
    print("OTA http server start !")

    cell_ota_enter_thread = threading.Thread(target=cell_entered_ota)
    cell_ota_enter_thread.start()




