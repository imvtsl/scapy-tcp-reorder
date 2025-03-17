# scapy-tcp-reorder

This repository contains source code and evidence for issue [#4696](https://github.com/secdev/scapy/issues/4696).

## Issue Description
When TCP segments are sent out of order, scapy's `srp1()` returns `None` for the last segment sent.

Expected behaviour: scapy's `srp1()` should return the `ACK` packet for the last segment sent as shown in packet capture. 

[issue.py](issue.py) is the TCP client to reproduce this issue.

[sample.pcap](sample.pcap) is the packet capture file. It shows ACK received from server for out of order packets.

[scapy_issue.PNG](scapy_issue.PNG) is the screenshot showing output of [issue.py](issue.py). It clearly shows that issue is reproduced. That is, scapy's `srp1` doesn't return the `ack` for out of order segment.

## Steps to reproduce:
- Set up your own TCP server.
- Replace dst_port, dst_ip, src_ip, src_mac, dst_mac, iface in [issue.py](issue.py)
- Capture on the interface using wireshark/tcpdump or any other tools of your choice.
- run issue.py
