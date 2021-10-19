import os
import subprocess

def resetConfig():
    ip_route_data = str(subprocess.check_output("ip route", shell=True)).split("\n")[-1].split(" ")
    dest_ip = ip_route_data[-2]
    wlan_details = ""
    dest_ip = ip_route_data[-2]
    for data in ip_route_data:
        if "wlan" in data:
            wlan_details = data
            break

    print(dest_ip)
    print(wlan_details)

resetConfig()