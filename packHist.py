import socket
import sys
from struct import *
import time
#import matplotlib.pyplot as plt
import os
try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
except Exception as e:
    print('Socket could not be created')
    sys.exit()
dicc = {1:"ICMP",6:"TCP",17:"UDP",54:"NARP",91:"LARP"}
types = []
count = []
for i in range(1000):
    packet = s.recvfrom(65565)
    packet = packet[0]
    eth_lenght = 14
    eth_header = packet[:eth_lenght]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])
    if(eth_protocol == 8):
        ip_header = packet[eth_lenght:20 + eth_lenght]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0XF
        iph_lenght = ihl * 4
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])
        if protocol in types:
            count[types.index(protocol)] += 1
        else:
            types.append(protocol)
            count.append(0)
dataFile = open("data.txt", "w")
ids = list(range(len(types)))
labels = []
for i in types:
    if not i in labels:
        labels.append(dicc[i])
dataFile.write(str(ids)+"|")
dataFile.write(str(count)+"|")
dataFile.write(str(labels))
#plt.bar(ids,count,color='g')
#plt.xticks(ids,labels)
#plt.show()
