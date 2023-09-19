import netfilterqueue
# iptables -I FORWARD -j NFQUEUE --queue-num 1
# iptables --flush
def process_packet(packet):
    print("hi")
    print(packet)
    packet.drop()

queue01 = netfilterqueue.NetfilterQueue()
queue01.bind(1,process_packet)
queue01.run()