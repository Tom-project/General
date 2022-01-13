# from typing import Annotated
#from re import A
import pefile
import os
import struct
import logging
import hashlib

i = 0
API_LIST = []
File = "C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe"
target = pefile.PE(File)

# ------------ Initialize Log file ------------
logging.basicConfig(filename='test1.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger('Test1')

# create console handler
ch = logging.StreamHandler()

# Format the log file
formatter = logging.Formatter('%(asctime)s - %(name)s- %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
    # ---------------------------------------------


def main():
    i = 0
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
    if ("GetProcAddress" in API_LIST):
        print("GetProcAddress Found")
        x = API_LIST.index("GetProcAddress")
        logger.info(API_LIST[x])
        x = input("Would you like to see the rest of the list? ")
        if x == "y":
            print(API_LIST)

    else:
        print(API_LIST)

    # --------------------------
    pe2 = pefile.PE("C:\Windows\System32\\amsi.dll")

    for section in pe2.sections:
        print(section.Name, "Virtual Address: ", hex(section.VirtualAddress), "Virtual Size: ",  hex(section.Misc_VirtualSize),
                    "Raw data size: ", section.SizeOfRawData )

        hash = hashlib.sha256()
        byt3s = []
        byt3s = pe2.sections[0].get_data() #read .text section append to byt3s 
        #print(byt3s)
        hash.update(byt3s)
        
        print("hash is: {0}".format(hash.hexdigest()))

    # ---------------------------
    


if __name__ == "__main__":
    main()