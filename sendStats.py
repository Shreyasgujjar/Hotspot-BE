import os
import time
import subprocess
import datetime
import requests
import csv
import json
import string
import random

endPoint = "https://handson.cs.odu.edu/hotspotapi/"



def check_and_send_ip():
    data = subprocess.check_output("arp -a", shell=True)
    devices = data.decode("utf-8").split("\n")
    print(devices)
    ips = []
    macs = []
    for device in devices[:-1]:
        if str(device).split(" ")[3] != "<incomplete>":
            ips.append(str(device).split(" ")[1][1:-1])
            macs.append(str(device).split(" ")[3])
            data = {
                "mac": str(device).split(" ")[3],
                "ip": str(device).split(" ")[1][1:-1]
            }
            # results = db.child("users").child("device-"+str(str(device).split(" ")[1][1:-1]).split(".")[3]).set(data)
    time.sleep(5)
    return ips, macs


def collectAndSendData(ip):
    data = subprocess.check_output("iptables -w -nvx -L vpnhotspot_acl", shell=True)
    bytesUsedData = data.decode("utf-8").split("\n")[2:-1]
    jsonToSend = {"ip": ip, "mainDeviceId": mainDeviceId}
    listOfDevices = []
    for data in bytesUsedData:
        a = data.split(" ")
        listOfDevices.append([x for x in a if x != ''])
    for data in listOfDevices:
        print(data)
        if data[-2] == ip:
            jsonToSend["dataIn"] = data[1]
        if data[-1] == ip:
            jsonToSend["dataOut"] = data[1]
    requests.post(endPoint + "device/updateData", json=jsonToSend)
    time.sleep(2)

ips, mac = check_and_send_ip()

for ip in ips:
    collectAndSendData(ip)