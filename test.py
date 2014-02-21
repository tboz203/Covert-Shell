#!/usr/bin/env python

from __future__ import print_function

import sys
import io
import threading
from subprocess import Popen, PIPE

def reader(so):
    try:
        print('this is fucking bullshit')
    except Exception as e:
        print('[-] Reader says:', e)

def writer(si):
    try:
        print('wtf')
    except Exception as e:
        print('[-] Writer says:', e)


write = threading.Thread(target=writer, args=['asdf'])
read = threading.Thread(target=reader, args=['lolol'])

print('[!] threads created')

write.start()
read.start()

print('[!] threads started')

write.join()
read.join()

print('[!] threads joined')
