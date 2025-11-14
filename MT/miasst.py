#!/usr/bin/python

import subprocess
import time
import json

for i, choice in enumerate(["Read Info", "ROMs that can be flashed", "Flash Official Recovery ROM", "Format Data", "Reboot"], start=1):
    print(f"\n\033[0;32m{i}\033[0m => {choice}")

while True:
    choice = input("\nEnter your \033[0;32mchoice\033[0m: ")
    if choice.isdigit() and 1 <= int(choice) <= 5:
        print("\n")
        break
    print("\nInvalid choice !\n")

subprocess.run(["pkill", "-9", "-f", "tcp"])

while True:
    # Get USB devices and parse JSON properly
    result = subprocess.run("termux-usb -l", shell=True, capture_output=True, text=True)
    devices_output = result.stdout.strip()
    
    if devices_output and devices_output != "[]":
        try:
            # Parse JSON to get device path
            devices_list = json.loads(devices_output)
            if devices_list:
                device_path = devices_list[0]  # Take first device
                
                # Request permission for the specific device
                result = subprocess.run(
                    f"$PREFIX/libexec/termux-api Usb -a permission --ez request true --es device {device_path}",
                    shell=True, capture_output=True, text=True
                )
                
                # Check if permission was granted - look for any positive response
                if result.returncode == 0 and result.stdout.strip():
                    print("Permission granted!")
                    break
                else:
                    print("\nGrant permission to termux-api")
        except:
            # Fallback if JSON parsing fails
            device_path = devices_output.replace('[', '').replace(']', '').replace('"', '').strip()
            if device_path and device_path.startswith('/dev/bus/usb/'):
                result = subprocess.run(
                    f"$PREFIX/libexec/termux-api Usb -a permission --ez request true --es device {device_path}",
                    shell=True, capture_output=True, text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    print("Permission granted!")
                    break
                else:
                    print("\nGrant permission to termux-api")
    else:
        for i in range(4):
            print(f"\rNo USB devices connected {'.' * (i % 4)}", end="")
            time.sleep(0.5)

# Use the properly extracted device path
subprocess.run(f"termux-usb -E -e '/data/data/com.termux/files/usr/bin/miasst_termux {choice}' -r {device_path}", shell=True)
