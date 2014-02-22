#!/usr/bin/env python

from __future__ import print_function

import sys
from random import randint
from time import sleep
from socket import socket, AF_INET, SOCK_RAW, IPPROTO_ICMP

from checksum import checksum

s = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

tobytes = lambda x: bytearray.fromhex('{:04x}'.format(x))
tohex = lambda x: ' '.join(['{:02x}'.format(item) for item in x])

mesg = bytearray('this is my message')
type_code = bytearray('\x08\x00')
# ident = tobytes(randint(0, 65535))
ident = tobytes(0)
fakecheck = bytearray('\x00\x00')

for i in range(256):
    seq = tobytes(i)
    realcheck = tobytes(checksum(type_code + fakecheck + ident + seq + mesg))
    data  = type_code + realcheck + ident + seq + mesg

    s.sendto(data, ('localhost', 0))

    sys.stdout.write('.')
    sys.stdout.flush()
    sleep(1)
