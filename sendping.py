#/usr/bin/env python

from socket import socket, AF_INET, SOCK_RAW, IPPROTO_ICMP
from random import randint
from checksum import checksum

def send_one(load):

    tobytes = lambda x: bytearray.fromhex('{:04x}'.format(x))
    tohex = lambda x: ' '.join(['{:02x}'.format(item) for item in x])

    mesg = bytearray(load)
    type_code = bytearray('\x08\x00')
    ident = tobytes(randint(0, 65535))
    fakecheck = bytearray('\x00\x00')

    seq = tobytes(0)
    realcheck = tobytes(checksum(type_code + fakecheck + ident + seq + mesg))
    data  = type_code + realcheck + ident + seq + mesg

    s = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
    s.sendto(data, ('localhost', 0))

