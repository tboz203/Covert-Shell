#!/usr/bin/env python

from __future__ import print_function

import sys
import io
import threading
from subprocess import Popen, PIPE

try:
    proc = Popen(args=['sh'], stdin=PIPE, stdout=PIPE)

    def reader(so):
        try:
            # buff = io.open(so.fileno())
            # while True:
            #     print(buff.next(), end='')
            while True:
                mesg = so.readline()
                print(mesg)
                if mesg == '':
                    break
        except Exception as e:
            print('[-] Reader says:', e)

    def writer(si):
        try:
            while True:
                mesg = raw_input()
                si.write(mesg)
        except Exception as e:
            print('[-] Writer says:', e)

    proc = Popen(args=['sh'], stdin=PIPE, stdout=PIPE)

    print('[!] proc created')

    try:
        write = threading.Thread(target=writer, args=[proc.stdin])
        read = threading.Thread(target=reader, args=[proc.stdout])
    except Exception as e:
        print('[!] exception while creating threads:', e)

    print('[!] threads created')

    write.start()
    read.start()

    print('[!] threads started')

    write.join()
    read.join()

    print('[!] threads joined')
except Exception as e:
    print('[!] fuck everything:', e)
