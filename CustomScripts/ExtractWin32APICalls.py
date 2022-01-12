from typing import Annotated
import pefile
import os
import struct

i = 0
API_LIST = []
File = "C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe"

target = pefile.PE(File)


# Pulls APIs from PE
for entry in target.DIRECTORY_ENTRY_IMPORT:
    for API in entry.imports:
        API_LIST.append(API.name)

# For some reason there was a load of Nill values in the list that broke my code when trying to decode
if None in API_LIST:
    while None in API_LIST:
        x = API_LIST.count(None)
        API_LIST.remove(API_LIST[x])

# Decoding from byte array
while(i < len(API_LIST)):
    API_LIST[i] = API_LIST[i].decode('utf-8')
    i = i + 1 

# Looking for Win API call of interest
if "GetProcAddress" in API_LIST:
    print("GetProcAddress Found")
    x = input("Would you like to see the rest of the list? ")
    if x == "y":
        print(API_LIST)


else:
    print(API_LIST)