import socket
import sys
from struct import *
import time
#import matplotlib.pyplot as plt
import os

fileData = open("ips.txt","r")
data = str(fileData.read())
# Convertir el string a diccionario
dic = eval(data)

try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
except Exception as e:
    print('Socket could not be created')
    sys.exit()

for i in range(100):
    packet = s.recvfrom(65565)
    # packet string from tuple
    packet = packet[0]
    # parse ethernet header
    eth_lenght = 14
    eth_header = packet[:eth_lenght]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])
    #print("Destination MAC: " + eth_addr(packet[0:6]) + " Src MAC: "  + eth_addr(packet[6:12]) + ' Protocol: ' + str(eth_protocol))

    # Parse IP packets, IP protocol number = 8

    if(eth_protocol == 8):
        # Parse IP header
        # Take first 20 chars for the ip header
        ip_header = packet[eth_lenght:20 + eth_lenght]
        # now unpack them :)
        iph = unpack('!BBHHHBBH4s4s', ip_header)

        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])
        if(dic.has_key(s_addr) and dic.has_key(d_addr)):
            if(dic[s_addr].has_key(d_addr)):
                dic[s_addr][d_addr] += 1
            else:
                dic[s_addr][d_addr] = 0
            print("src: " + str(s_addr) + " dest: " + str(d_addr))

#print(dic)
dataFile = open("ips.txt", "w")
dataFile.write(str(dic))
dataFile.close()
