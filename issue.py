from scapy.all import *
import random

src_port = random.randint(1024,65535)
dst_port = 44444

seq = random.randint(0, 2**32-1)

dst_ip ='192.168.50.1'
src_ip = '192.168.50.234'

src_mac = '11:22:33:dd:ee:ff'
dst_mac = '08:00:27:65:be:ef'

iface = 'enp0s9'

eth = Ether(src=src_mac, dst=dst_mac)

ip = IP(src=src_ip, dst=dst_ip)

syn = TCP(sport=src_port, dport=dst_port, flags='S', seq=seq)
syn_ack = srp1(eth/ip/syn, iface=iface)

server_seq = syn_ack[TCP].seq

seq = syn_ack[TCP].ack
ack_num = server_seq+1
ack = TCP(sport=src_port, dport=dst_port, flags='A', seq=seq, ack=ack_num)
sendp(eth/ip/ack, iface=iface)

print('handshake completed')

# send one segment
data = 'abc'
data_pkt = TCP(sport=src_port, dport=dst_port, flags='PA', seq=seq, ack=ack_num)/data
data_ack = srp1(eth/ip/data_pkt, iface=iface)

print('data pkt sent')

seq = data_ack[TCP].ack
ack_num = data_ack[TCP].seq


# reorder next two segments
order_2_data = 'ghi'
order_2_pkt = TCP(sport=src_port, dport=dst_port, flags='PA', seq=seq+3, ack=ack_num)/order_2_data
order_2_ack = srp1(eth/ip/order_2_pkt, iface=iface, timeout=5)

order_1_data = 'def'
order_1_pkt = TCP(sport=src_port, dport=dst_port, flags='PA', seq=seq, ack=ack_num)/order_1_data
order_1_ack = srp1(eth/ip/order_1_pkt, iface=iface, timeout=5)

# this was acked with final correct seq number as seen in wireshark, but scapy doesn't show it

if not order_1_ack:
    print('issue reproduced')
else:
    print('issue not reproduced')

# server closes connection when newline is received, so sending newline
final_data = 'bye!\n'
final_data_pkt = TCP(sport=src_port, dport=dst_port, flags='PA', seq=seq+6, ack=ack_num)/final_data
fin_ack = srp1(eth/ip/final_data_pkt, iface=iface, timeout=5)



