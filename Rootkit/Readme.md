# Overview
This is the source code for a linux rootkit, aimed at providing elevated persistence on a system with some detection evasion through hiding the module from userspace programs such as lsmod.

# Why
I wrote this program to gain a btter understanding of linux kernels. Writing this software helped me understand how basic system functions like mkdir, sys_read, or kill actually work at the kernel level, as well as implementing code to interact with the kernel and interacting with the userspace from the kernel.

# How to use
I made a pdf in this repo to goes over basic linux kernel stuff as well as compilation and installing, but using the following make file will compile it into a module thats loadable.

```bash
obj-m = rootkitHook.o

KVERSION = 5.14.0-kali4-amd64

all:
        make -C /lib/modules/$(KVERSION)/build M=$(PWD) modules

clean:
        make -C /lib/modules/$(KVERSION)/build M=$(PWD) clean

```

Once you have a .ko file you can run ``` sudo insmod rootkitHook.ko``` and ``` sudo rmmod rootkitHook ``` to unload the module.
