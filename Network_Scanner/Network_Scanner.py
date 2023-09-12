import scapy.all as sp
import argparse


def get_argument():
    arg = argparse.ArgumentParser()
    arg.add_argument("-t", "--target", dest="target", help="Target IP/IP range.")
    options = arg.parse_args()
    return options


def scan(ip):
    arp_request = sp.ARP()
    arp_request.pdst = ip
    broadcast = sp.Ether()
    broadcast.dst = 'ff:ff:ff:ff:ff:ff'

    final_packet = broadcast / arp_request
    # print(final_packet.summary())
    clients_list = sp.srp(final_packet, timeout=1, verbose=False)[0]  # verbose will not give the line (statement)
    # print(clients_list.summary())
    print("IP\t\t\t MAC address\n--------------------------------------------")
    for element in clients_list:
        print(element[1].psrc, "\t\t", element[1].hwsrc)  # (sent,received) so(0,1) psrc=source tp and hwsrc=MAC address

    #     clients_dict={"ip":element[1].psrc,"mac":element[1].hwsrc}
    #     lists.append(clients_dict)
    # return lists


# def print_result(results_list):
#     print("IP\t\t\tMAC address\n--------------------------------------------")
#     for client in results_list:
#         print(client["ip"] + "\t\t" + client["mac"])
# scan_result=scan("192.168.37.1/24")
# print_result(scan_result)
print("\t\t\t\t«Welcome to Network Scanner»  \n \t\t\t\t\t\t\t\t\t [☣]Harsha D B")
options = get_argument()
scan(options.target)
