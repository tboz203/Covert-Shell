#!/usr/bin/env python

from __future__ import print_function
import time
import socket

def deconstruct(data):
    class Empty(object):
        pass

    ip2str = lambda s: '%i.%i.%i.%i' % (ord(s[0]), ord(s[1]), ord(s[2]), ord(s[3]))
    ip2str2 = lambda s: '%i.%i.%i.%i' % [map(ord, s)]
    b2hex = lambda b: ' '.join('{:02x}'.format(ord(item)) for item in b)

    output = Empty()

    output.ip_header = ip_header = data[:20]
    output.icmp_header = icmp_header = data[20:]

    output.src = ip_header[-8:-4]
    output.srcstr = ip2str(output.src)
    output.dst = ip_header[-4:]
    output.dststr = ip2str(output.dst)

    output.type = ord(icmp_header[0])
    output.code = ord(icmp_header[1])
    output.cksum = b2hex(icmp_header[2:4])
    output.head_data = icmp_header[4:8]
    output.load = icmp_header[8:]
    output.echop = (output.type in (0, 8) and output.code == 0)

    if output.echop:
        output.reqp = (output.type == 8)
        output.id = b2hex(output.head_data[:2])
        output.seq = b2hex(output.head_data[2:])


    # # this was a quick attempt to do data descriptors, but i decided against
    # # it, after having finished. so yeah...
    # echop = lambda a, b: ord(a) in (0, 8) and ord(b) == 0
    # noset = lambda s, o, v: raise AttributeError()

    # output.id = Empty()
    # output.id.__get__ = lambda s, p, t=None: p.head_data[:2] if echop(p.type, p.code) else None
    # output.id.__set__ = noset

    # output.seq = Empty()
    # output.seq.__get__ = lambda s, p, t=None: p.head_data[2:] if echop(p.type, p.code) else None
    # output.seq.__set__ = noset

    return output

def get_one():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.bind(('', 1))

    while True:
        data = sock.recv(1024)
        packet = deconstruct(data)
        if packet.echop:
            return packet



if __name__ == '__main__':
    # Open a raw socket listening on all ip addresses
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.bind(('', 1))

    try:
        while True:
            # receive data
            data = sock.recv(1024)

            # # ip header is the first 20 bytes
            # ip_header = data[:20]

            # # ip source address is 4 bytes and is second last field (dest addr is last)
            # ips = ip_header[-8:-4]

            # # convert to dotted decimal format
            # source = '%i.%i.%i.%i' % (ord(ips[0]), ord(ips[1]), ord(ips[2]), ord(ips[3]))

            # print('Ping from %s' % source)

            packet = deconstruct(data)

            print('src = ' + packet.srcstr, end=', ')
            print('dst = ' + packet.dststr, end=', ')

            if packet.echop:
                if packet.reqp:
                    print('echo request', end=', ')
                else:
                    print('echo reply', end=', ')
                print('id = ' + packet.id, end=', ')
                print('seq = ' + packet.seq, end=', ')

            print()

    except KeyboardInterrupt :
        print()
