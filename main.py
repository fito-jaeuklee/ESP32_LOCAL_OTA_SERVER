import threading
from tkinter import filedialog
import time
import platform
import subprocess
import server as ota
import cell_on_off_control as cell_on_off
import socket


def check_wifi_ssid_ip_setting():
    try:
        print(platform.system())
        if platform.system() == "Windows":
            command = "netsh wlan show networks interface=Wi-Fi"
        elif platform.system() == "Linux":
            command = "nmcli dev wifi list"
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

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(s.getsockname()[0])
        ip = s.getsockname()[0]
        s.close()

        if '192.168.1.254' in ip:
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
        time.sleep(110)
        print("ota success / fail flag = ", ota.OTA_flag)

        ota.save_ota_done(0)


# TODO:
if __name__ == '__main__':
    check_wifi_ssid_ip_setting()
    path = filedialog.askdirectory()
    print(path)
    ota_thread = threading.Thread(target=ota.ota_server_open, args=[path])

    ota_thread.start()
    print("OTA http server start !")

    cell_ota_enter_thread = threading.Thread(target=cell_entered_ota)
    cell_ota_enter_thread.start()




