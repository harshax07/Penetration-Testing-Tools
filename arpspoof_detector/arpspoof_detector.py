import scapy.all as sp


def get_mac(ip):
    arp_request = sp.ARP()
    arp_request.pdst = ip
    broadcast = sp.Ether()
    broadcast.dst = 'ff:ff:ff:ff:ff:ff'
    final_packet = broadcast / arp_request
    clients_list = sp.srp(final_packet, timeout=1, verbose=False)[0]
    return clients_list[0][1].hwsrc


def sniff(interface):
    sp.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(sp.ARP) and packet[sp.ARP].op == 2:
        try:
            real_mac = get_mac(packet[sp.ARP].psrc)
            response_mac = packet[sp.ARP].hwsrc

            if real_mac != response_mac:
                print("[!] You are under attack ")
            else:
                print("[+] You ARP table is secured")
        except IndexError:
            pass


interface_input = input("Enter the interface: ")
sniff(interface_input)
