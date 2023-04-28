import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore


#Types:
# 0: Invalid / Null
# 1: Hello Packet
# 2: Hello ACK Packet
# 3: Mulicast Packet
# 4: Unicast Packet

# Nothing works right now, like at all
# The objective would be to store everything in a struct, but since we have different packet types of varying lengths 


def create_LSA_packet(pkttype, seq, TTL, src, hops, advRoute, LSSeq, CRC):
    #Type(1), Len(4), Seq(1), TTL(1), src(1), hops(1), advRoute(4), LSSeq(4), CRC(1)
    #header (18)
    header = struct.pack('BBBsBLLB', pkttype, seq, TTL, src, hops, advRoute, LSSeq, CRC)
    return header

def create_unicast_packet(pkttype, seq, TTL, src, dst, data):
    #Type(1), Len(4), Seq(1), TTL(1), src(4), dst(4), data(1-1480)
    #header (15) + data(1-1480) -> 16 - 1495
    pktlength = len(data)
    header = struct.pack('BLBB15s15s', pkttype, pktlength, seq, TTL, src, dst)
    
    return header + bytes(data, 'utf-8')
    

def create_multicast_packet(pkttype, seq, TTL, kval, dst1, dst2, dst3, data):
    """Create new packet with given fields"""
    #Type(1), Len(4), Seq(1), TTL(1), K-val(1), Dest1(4), Dest2(4), Dest3(4), Data(1-1480)
    #header (16) + data(1-1480) -> 17 - 1496
    pktlength = len(data)
    header = struct.pack('BLBBBsss', pkttype, pktlength, seq, TTL, kval, dst1, dst2, dst3)
    return header + bytes(data, 'utf-8')


def read_header(pkt):
    #change bytes to account for network encapsulations
    
    header = pkt[0:39] #not sure if this is the correct size, will have to revisit and change
    print(header)
    pkttype, pktlength, seq, TTL, src, dst = struct.unpack('BLBB15s15s', header)
    return pkttype, pktlength, seq, TTL, src, dst

def read_data(pkt):
    #change bytes to account for network encapsulations
    data = pkt[16:]
    return data

def main():
    print(struct.calcsize('BLBB15s15s'))
    
    myPkt = create_unicast_packet(1, 1, 5, b"192.168.1.5", b"192.168.1.7", "WHAAAT")
    
    pkttype, pktlength, seq, TTL, src, dst = read_header(myPkt)
    
    print(pkttype)
    print(pktlength)
    print(seq)
    print(TTL)
    print(src)
    print(dst)
    

    

if __name__ == "__main__":
    main()
