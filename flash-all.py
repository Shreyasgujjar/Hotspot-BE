import subprocess
import os
import time

list_to_be_flashed = ["LOGO", "aop", "system", "vbmeta", "xbl", "abl", "bluetooth", "dtbo", "modem", "tz", "system", "vendor"]
devices = []
unlockedDevices = []
completedFlashDevices = []

# data = subprocess.check_output("ls /Users/shre/Downloads/payload_dumper/output", shell=True).decode("utf-8").split("\n")

currentStatus = {}

devicesConnected = subprocess.check_output("adb devices", shell=True).decode("utf-8").split("\n")
for data in devicesConnected[1:-2]:
    devices.append(data.split("\t")[0])
    currentStatus[data.split("\t")[0]] = {
        "adbId": data.split("\t")[0],
        "stage": 0,
        "imei": subprocess.check_output('''adb -s ''' + data.split("\t")[0] + ''' shell service call iphonesubinfo 1 | awk -F "'" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS=''', shell=True).decode("utf-8").strip()
    }
    os.system("adb -s " + data.split("\t")[0] + " reboot bootloader")
    print("Rebooted " + data.split("\t")[0] + " to bootloader")
    time.sleep(1)

print("Waiting for all phones to reach bootloader stage")
time.sleep(10)

devicesConnected = subprocess.check_output("adb devices", shell=True).decode("utf-8").split("\n")
for data in devicesConnected[1:-2]:
    os.system("adb -s " + data.split("\t")[0] + " reboot bootloader")

while True:
    data = subprocess.check_output("fastboot devices", shell=True).decode("utf-8").split("\n")
    for ids in data[:-1]:
        if ids.split("\t")[0] not in unlockedDevices:
            print("Unlocking device - " + ids.split("\t")[0])
            os.system("fastboot -s " + ids.split("\t")[0] + " flash cust-unlock /Users/shre/Downloads/payload_dumper/unlockCodes/unlock_code_" + currentStatus[ids.split("\t")[0]]["imei"] + ".bin")
            time.sleep(1)
            os.system("fastboot -s " + ids.split("\t")[0] + " oem unlock")
            unlockedDevices.append(ids.split("\t")[0])
            print("Unlocked device - " + ids.split("\t")[0])
    if len(devices) == len(unlockedDevices):
        print("Unlocked all devices")
        break
    time.sleep(2)

unlockedDevices = []
print("Waiting for 20 seconds...")
time.sleep(20)
print("Trying to flash the devices")

while True:
    data = subprocess.check_output("fastboot devices", shell=True).decode("utf-8").split("\n")
    for ids in data[:-1]:
        if ids.split("\t")[0] not in unlockedDevices:
            os.system("adb -s " + key + " reboot bootloader")
            unlockedDevices.append(ids.split("\t")[0])
    if len(devices) == len(unlockedDevices):
        print("Restarted all devices")
        break

while True:
    data = subprocess.check_output("fastboot devices", shell=True).decode("utf-8").split("\n")
    for ids in data[:-1]:
        if ids.split("\t")[0] not in completedFlashDevices:
            if currentStatus[ids.split("\t")[0]]["stage"] + 1 != len(list_to_be_flashed):
                print("Flashing stage - " + list_to_be_flashed[currentStatus[ids.split("\t")[0]]["stage"]] + " for device - " + ids.split("\t")[0])
                os.system("fastboot -s " + ids.split("\t")[0] + " flash " + list_to_be_flashed[currentStatus[ids.split("\t")[0]]["stage"]] + " /Users/shre/Downloads/payload_dumper/output/" + list_to_be_flashed[currentStatus[ids.split("\t")[0]]["stage"]] + ".img")
                currentStatus[ids.split("\t")[0]]["stage"] = currentStatus[ids.split("\t")[0]]["stage"] + 1
            else:
                print("Completed device with id - " + ids.split("\t")[0] + " booting now")
                os.system("fastboot -s" + ids.split("\t")[0] + " boot /Users/shre/Downloads/payload_dumper/output/boot.img")
                completedFlashDevices.append(ids.split("\t")[0])
    if len(completedFlashDevices) == len(devices):
        print("Completed flashing all devices")
        break;
    time.sleep(5)

for device in completedFlashDevices:
    print("Sending the System Update file to phone - " + device)
    os.system("adb -s " + device + " /Users/shre/Downloads/OnePlus6TOxygen.zip /sdcard/Download/")