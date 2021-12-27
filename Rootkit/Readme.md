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

# References / Honerable mentions
This was a project i did not complete alone, i used lots of online resources to help me make it, and so i feel they should be mentioned.

- [Writing a Linux Kernel Module — Part 1: Introduction | derekmolloy.ie](http://derekmolloy.ie/writing-a-linux-kernel-module-part-1-introduction/)
- [,ch02.6536 (lwn.net)](https://static.lwn.net/images/pdf/LDD3/ch02.pdf)
- [Kernel RootKits. Getting your hands dirty - Malware - 0x00sec - The Home of the Hacker](https://0x00sec.org/t/kernel-rootkits-getting-your-hands-dirty/1485)
- [Linux Rootkits Part 2: Ftrace and Function Hooking :: TheXcellerator](https://xcellerator.github.io/posts/linux_rootkits_02/)
- [Hooking Linux Kernel Functions, Part 2: How to Hook Functions with Ftrace - CodeProject](https://www.codeproject.com/Articles/1275114/Hooking-Linux-Kernel-Functions-Part-2-How-to-Hook)