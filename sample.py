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
r = requests.get(endPoint + "device/sample")

os.system("cd /sdcard/Download/hotspot-be/ && git pull")

mainDeviceId = ""

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def deleteOldConfig(dest_ip):
    wlan_details = ""
    for data in ip_route_data:
        if "wlan" in data:
            wlan_details = data
            break
    os.system("iptables -w -t nat -D vpnhotspot_masquerade -s " + dest_ip + "/24 -o rmnet_data2 -j MASQUERADE")
    print("iptables -w -t nat -D vpnhotspot_masquerade -s " + dest_ip + "/24 -o rmnet_data2 -j MASQUERADE")
    os.system("iptables -w -t nat -D vpnhotspot_masquerade -s " + dest_ip + "/24 -o tun0 -j MASQUERADE")
    print("iptables -w -t nat -D vpnhotspot_masquerade -s " + dest_ip + "/24 -o tun0 -j MASQUERADE")
    os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
    print("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
    os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
    print("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")

def addNewConfig(dest_ip):
    wlan_details = ""
    for data in ip_route_data:
        if "wlan" in data:
            wlan_details = data
            break
    os.system("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o rmnet_data2 -j MASQUERADE")
    print("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o rmnet_data2 -j MASQUERADE")
    os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    os.system("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o tun0 -j MASQUERADE")
    print("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o tun0 -j MASQUERADE")
    os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    print("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    print("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
    print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
    os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
    print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")

def turnOnVPNHotspot():
    try:
        requests.get(endPoint + "log/deviceId/" + mainDeviceId)
        data = subprocess.check_output("ip rule | grep 17980", shell=True)
        requests.get(endPoint + "log/deviceId/" + mainDeviceId + "/gotiprule")
        f = open("/sdcard/Download/hotspot-be/whitelisted.txt", "r")
        requests.get(endPoint + "log/deviceId/" + mainDeviceId + "/gotwhitelisteddata")
        ip_route_data = str(subprocess.check_output("ip route", shell=True)).split("\n")[-1].split(" ")
        old_ip = f.read()
        dest_ip = ip_route_data[-2]
        requests.get(endPoint + "log/deviceId/" + str(old_ip) + str(dest_ip))
        if old_ip != dest_ip:
            deleteOldConfig(old_ip)
            addNewConfig(dest_ip)
            print("Ip had changed so I have done the neccessary changes")
            f = open("/sdcard/Download/hotspot-be/whitelisted.txt", "w")
            f.write(dest_ip)
            f.close()
        else:
            print("The Dest IP is the same")
        print("VPN routing is already enabled")
        checkAndAuthoriseDevices()
    except subprocess.CalledProcessError: 
        requests.get(endPoint + "log/deviceId/startinghotspotnow")
        os.system("ndc ipfwd enable vpnhotspot_wlan0")
        os.system("iptables -w -N vpnhotspot_fwd")
        os.system("iptables -w -N vpnhotspot_acl")
        os.system("iptables -w -t filter -I FORWARD -j vpnhotspot_fwd")
        ip_route_data = str(subprocess.check_output("ip route", shell=True)).split("\n")[-1].split(" ")
        # number = subprocess.check_output("cat /sys/class/net/tun0/ifindex", shell=True).decode("utf-8").split("\n")[0]
        # number = str(int(number) + 1000)
        lookUpName = subprocess.check_output("iptables -S | grep -E 'bw_INPUT.*rmnet'", shell=True).decode("utf-8").split(" ")[3]
        lookUpNumber = int(subprocess.check_output("cat /sys/class/net/" + lookUpName + "/ifindex", shell=True).decode("utf-8")) + 1000
        wlan_details = ""
        dest_ip = ip_route_data[-2]
        for data in ip_route_data:
            if "wlan" in data:
                wlan_details = data
                break
        print("Executed first few statements");
        os.system("iptables -w -t filter -I vpnhotspot_fwd -i " + wlan_details + " -j vpnhotspot_acl")
        print("iptables -w -t filter -I vpnhotspot_fwd -i " + wlan_details + " -j vpnhotspot_acl")
        os.system("iptables -w -t filter -I vpnhotspot_fwd -o " + wlan_details + " -m state --state ESTABLISHED,RELATED -j vpnhotspot_acl")
        print("iptables -w -t filter -I vpnhotspot_fwd -o " + wlan_details + " -m state --state ESTABLISHED,RELATED -j vpnhotspot_acl")
        os.system("iptables -w -t filter -A vpnhotspot_fwd -i " + wlan_details + " ! -o " + wlan_details + " -j REJECT")
        print("iptables -w -t filter -A vpnhotspot_fwd -i " + wlan_details + " ! -o " + wlan_details + " -j REJECT")
        os.system("iptables -w -t nat -N vpnhotspot_masquerade")
        print("iptables -w -t nat -N vpnhotspot_masquerade")
        os.system("iptables -w -t nat -I POSTROUTING -j vpnhotspot_masquerade")
        print("iptables -w -t nat -I POSTROUTING -j vpnhotspot_masquerade")
        os.system("/system/bin/ip rule add  iif " + wlan_details + " unreachable priority 17980")
        print("/system/bin/ip rule add  iif " + wlan_details + " unreachable priority 17980")
        os.system("ip rule add  iif " + wlan_details + " lookup " + str(lookUpNumber) + " priority 17900")
        print("ip rule add  iif " + wlan_details + " lookup " + str(lookUpNumber) + " priority 17900")
        os.system("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o " + lookUpName + " -j MASQUERADE")
        print("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o " + lookUpName + " -j MASQUERADE")
        os.system("/system/bin/ip rule add to 198.224.137.129 iif " + wlan_details + " lookup " + str(lookUpNumber) + " priority 17700")
        print("/system/bin/ip rule add to 198.224.137.129 iif " + wlan_details + " lookup " + str(lookUpNumber) + " priority 17700")
        os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        # os.system("/system/bin/ip rule add  iif " + wlan_details + " lookup " + number + " priority 17800")
        # print("/system/bin/ip rule add  iif " + wlan_details + " lookup " + number + " priority 17800")
        # os.system("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o tun0 -j MASQUERADE")
        # print("iptables -w -t nat -A vpnhotspot_masquerade -s " + dest_ip + "/24 -o tun0 -j MASQUERADE")
        # os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        # print("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        # os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        # print("iptables -w -t nat -D PREROUTING -i " + wlan_details + " -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
        # os.system("/system/bin/ip rule del to 198.224.137.129 iif " + wlan_details + " lookup 1011 priority 17700")
        # print("/system/bin/ip rule del to 198.224.137.129 iif " + wlan_details + " lookup 1011 priority 17700")
        # os.system("system/bin/ip rule add to 208.67.222.222 iif " + wlan_details + " lookup " + number + " priority 17700 ")
        # print("system/bin/ip rule add to 208.67.222.222 iif " + wlan_details + " lookup " + number + " priority 17700 ")
        # os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
        # print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
        # os.system("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
        # print("iptables -w -t nat -A PREROUTING -i " + wlan_details + " -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 208.67.222.222")
        f = open("/sdcard/Download/hotspot-be/whitelisted.txt", "w")
        f.write(dest_ip)
        f.close()
        checkAndAuthoriseDevices()

def checkAndAuthoriseDevices():
    ips, macs = check_and_send_ip()
    ip_route_data = str(subprocess.check_output("ip route", shell=True)).split("\n")[-1].split(" ")
    # number = subprocess.check_output("cat /sys/class/net/tun0/ifindex", shell=True).decode("utf-8").split("\n")[0]
    # number = str(int(number) + 1000)
    wlan_details = ""
    dest_ip = ip_route_data[-2]
    for data in ip_route_data:
        if "wlan" in data:
            wlan_details = data
            break
    print("Checking to authorise devices")
    dataToSend = []
    for i in range(0, len(ips)):
        newData = {}
        r = requests.get(endPoint + "device/getall/" + mainDeviceId + "/" + ips[i])
        try:
            deviceData = dict(r.json())
            print(deviceData)
            newData["mainDeviceId"] = mainDeviceId
            newData["deviceIp"] = ips[i]
            newData["deviceMac"] = macs[i]
            if len(deviceData["data"]) != 0:
                if deviceData["data"][0]["authorised"] == True:
                    if not Authorised(ip):
                        print("At - " + str(datetime.datetime.now()))
                        dataToSend.append(newData)
                        os.system("iptables -w -t filter -I vpnhotspot_acl -i " + wlan_details + " -s " + ip + " -j ACCEPT")
                        print("iptables -w -t filter -I vpnhotspot_acl -i " + wlan_details + " -s " + ip + " -j ACCEPT")
                        os.system("iptables -w -t filter -I vpnhotspot_acl -o " + wlan_details + " -d " + ip + " -j ACCEPT")
                        print("iptables -w -t filter -I vpnhotspot_acl -o " + wlan_details + " -d " + ip + " -j ACCEPT")
                    else:
                        collectAndSendData(ip)
                        print("The ip - " + ip + " is already authorised")
                else:
                    if Authorised(ip):
                        deauthoriseDevice(ip)
                        print("Deauthorised - " + ip)
                    else:
                        print("IP - " + ip + " not in the Authorised list to deauthorise")
            r = requests.post(endPoint + "device/checkandcreate", json=newData)
            print(r)
        except json.decoder.JSONDecodeError:
            print("There was a processing the request")

def Authorised(ip):
    try:
        data = subprocess.check_output("iptables -S | grep " + ip, shell=True)
        acceptedConnections = data.decode("utf-8").split("\n")
        if len(acceptedConnections) == 0:
            return False
        else:
            return True
    except:
        return False



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

def deauthoriseDevice(deviceIpToDeAuthorise):
    wlan_details = ""
    dest_ip = ip_route_data[-2]
    for data in ip_route_data:
        if "wlan" in data:
            wlan_details = data
            break
    os.system("iptables -w -t filter -D vpnhotspot_acl -o " + wlan_details + " -d " + deviceIpToDeAuthorise + " -j ACCEPT")
    print("iptables -w -t filter -D vpnhotspot_acl -o " + wlan_details + " -d " + deviceIpToDeAuthorise + " -j ACCEPT")
    os.system("iptables -w -t filter -D vpnhotspot_acl -i " + wlan_details + " -s " + deviceIpToDeAuthorise + "  -j ACCEPT")
    print("iptables -w -t filter -D vpnhotspot_acl -i " + wlan_details + " -s " + deviceIpToDeAuthorise + "  -j ACCEPT")


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


print("Trying to run the commands")
data = subprocess.check_output("arp -a", shell=True)
devices = data.decode("utf-8").split("\n")
print(devices)
for device in devices[:-1]:
    if str(device).split(" ")[3] != "<incomplete>":
        data = {
            "mac": str(device).split(" ")[3],
            "ip": str(device).split(" ")[1][1:-1]
        }
        # results = db.child("users").child("device-"+str(str(device).split(" ")[1][1:-1]).split(".")[3]).set(data)
        # if str(device).split(" ")[3] != "86:52:44:96:cb:3d":
        #     os.system("arp -s " + str(device).split(" ")[1][1:-1] + " " + str(RandMac()))
wlan = ""
ip_route_data = str(subprocess.check_output("ip route", shell=True)).split("\n")[-1].split(" ")
dest_ip = ip_route_data[-2]

if os.path.isfile("/sdcard/Download/hotspot-be/uniqueid.txt"):
    f = open("/sdcard/Download/hotspot-be/uniqueid.txt", "r")
    mainDeviceId = f.read()
else:
    mainDeviceId = id_generator()
    f = open("/sdcard/Download/hotspot-be/uniqueid.txt", "w")
    f.write(mainDeviceId)

for data in ip_route_data:
    if "wlan" in data:
        wlan = data
        break
if wlan == "":
    print("Wifi is not connected")
    requests.get(endPoint + "sample/HotspotNotOn")
else:
    turnOnVPNHotspot()
    # try:
    #     number = 0
    #     data = subprocess.check_output("ls /sys/class/net", shell=True).decode("utf-8").split("\n")
    #     print(data)
    #     for tun in data:
    #         if "tun" in tun:
    #             number = subprocess.check_output("cat /sys/class/net/" + tun + "/ifindex", shell=True).decode("utf-8").split("\n")[0]
    #     if number != 0:
    #         turnOnVPNHotspot()
    #     else:
    #         print("VPN is not connected")
    #         requests.get(endPoint + "sample/VPNNotConnected")
    # except subprocess.CalledProcessError: 
    #     print("VPN is not connected")
    #     requests.get(endPoint + "sample/VPNNotConnected")
