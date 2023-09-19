import scapy.all as sp
from scapy.layers import http


def sniff(interface):
    sp.sniff(iface=interface, store=False, prn=sniffed_packet)


def sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):

sniff("wlan0")
