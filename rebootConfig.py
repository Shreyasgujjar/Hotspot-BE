import os
import subprocess

def resetConfig():
    ip_route_data = str(subprocess.check_output("ip route", shell=True)).split("\n")[-1].split(" ")
    dest_ip = ip_route_data[-2]
    lookUpName = subprocess.check_output("iptables -S | grep -E 'bw_INPUT.*rmnet'", shell=True).decode("utf-8").split(" ")[3]
    lookUpNumber = int(subprocess.check_output("cat /sys/class/net/" + lookUpName + "/ifindex", shell=True).decode("utf-8")) + 1000
    connectedDevices = subprocess.check_output("iptables -S | grep -E 'vpnhotspot_acl -d'", shell=True).decode("utf-8").split("\n")
    wlan_details = ""
    dest_ip = ip_route_data[-2]
    for data in ip_route_data:
        if "wlan" in data:
            wlan_details = data
            break

    print(dest_ip)
    print(wlan_details)
    print(lookUpNumber)
    print(lookUpName)
    for data in connectedDevices:
        if data != '':
            os.system("iptables -w -t filter -D vpnhotspot_acl -o " + wlan_details + " -d " + data.split(" ")[3].split("/")[0] + " -j ACCEPT")
            print(data.split(" ")[3].split("/")[0])
    os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details +" -p udp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    os.system("iptables -w -t nat -D PREROUTING -i " + wlan_details +" -p tcp -d " + dest_ip + " --dport 53 -j DNAT --to-destination 198.224.137.129")
    os.system("/system/bin/ip rule del to 198.224.137.129 iif " + wlan_details + " lookup " + str(lookUpNumber) + " priority 17700")
    os.system("iptables -w -t nat -D vpnhotspot_masquerade -s " + dest_ip + "/24 -o " + lookUpName + " -j MASQUERADE")
    os,system("/system/bin/ip rule del  iif " + wlan_details + " lookup " + lookUpNumber + " priority 17900")
    os.system("/system/bin/ip rule del  iif " + wlan_details + " unreachable priority 17980")
    os.system("cleiptables -w -t nat -D POSTROUTING -j vpnhotspot_masquerade")
    os.system("iptables -w -t filter -D vpnhotspot_fwd -i " + wlan_details + " ! -o " + wlan_details + " -j REJECT")
    os.system("iptables -w -t filter -D vpnhotspot_fwd -o " + wlan_details + " -m state --state ESTABLISHED,RELATED -j vpnhotspot_acl")
    os.system("iptables -w -t filter -D vpnhotspot_fwd -i " + wlan_details + " -j vpnhotspot_acl")
    os.system("iptables -w -t filter -D FORWARD -j vpnhotspot_fwd")
    os.system("ndc ipfwd disable vpnhotspot_wlan0")

resetConfig()