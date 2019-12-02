import socket
import sys
from struct import *
import time


try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
except Exception as e:
    print('Socket could not be created')
    sys.exit()
tams = []
count = []
for i in range(1000):
    packet = s.recvfrom(65565)
    packet = packet[0]
    eth_lenght = 14
    eth_header = packet[:eth_lenght]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])

    if(eth_protocol == 8):
        tam = len(packet)
        if tam in tams:
            count[tams.index(tam)] += 1
        else:
            tams.append(tam)
            count.append(0)
dataFile = open("data2.txt", "w")
dataFile.write(str(tams)+"|")
dataFile.write(str(count))
        #print("Version: " + str(version) + " IP Header lenght: " + str(ihl) + " TTL: " + str(ttl) + " Protocol: " + str(protocol) + " Source address: " + str(s_addr) + " Destination address: " + str(d_addr))
