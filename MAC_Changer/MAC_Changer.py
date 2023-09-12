#!/usr/bin/env python
import subprocess
import optparse
import re


def taking_input():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (option, argum) = parser.parse_args()
    interface = option.interface
    new_mac = option.new_mac
    if not option.interface and not option.new_mac:
        interface = input("Enter the interface: ")
        new_mac = str(input("Enter the new mac: "))
    elif not option.interface:
        parser.error("[-] Please specify an interface, use --help to get more info.")
    elif not option.new_mac:
        parser.error("[-] Please specify a New MAC, use --help to get more info.")

    return (interface, new_mac)


def mac_chr(interface, new_mac):
    print("[+] Changing the MAC address..")
    print("[+] Interface :" + interface)
    # subprocess.call("ifconfig "+interface+" down", shell=True)
    # subprocess.call("ifconfig "+interface+" hw ether "+new_mac, shell=True)
    # subprocess.call("ifconfig "+interface+" up", shell=True)
    # secure way:
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    # print("[+] Mac address changed to " + new_mac)


def current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig", interface])
    ifconfig_output = str(ifconfig_output)
    mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)
    if mac_search:
        return mac_search.group(0)
    else:
        print("[-] Could not search MAC address.Try again with different Interface")
        exit()


print("\t\t\t\t«Welcome to MAC Changer»  \n \t\t\t\t\t\t\t\t\t [☣]Harsha D B")
(interface, new_mac) = taking_input()  # calling the function and reserving the values

c_mac = current_mac(interface)
print("Current MAC Address of", str(interface), "is: ", str(c_mac))

mac_chr(interface, new_mac)  # calling the mac_chr() function and sending values recieved from the taking_input()

c_mac = current_mac(interface)
if c_mac == new_mac:
    print("[+] MAC address successfully changed to", c_mac)
else:
    print("[-] MAC address could not change...Try again")
