import pefile
import os
import struct
import logging
import hashlib
import time
import threading
import csv

#i = 0
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

def extractResults(dataArr2,dataArr):
    header = ['LogData', 'Occur?', 'priority']
    data =[
            [dataArr2],
            [dataArr]
          ]
    with open(r"C:\\Users\\thoma\Documents\dataset.csv", "w") as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(header)
        writer.writerows(data)


def APIPull():
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
        x = API_LIST.index("GetProcAddress") # Locate where in the array the API call is
        logger.info(API_LIST[x]) # Append to log file
        b = input("Would you like to see the rest of the list? ")
        if b == "y":
            print(API_LIST)
        dataArr2 = [API_LIST[x],"yes","medium"]
        extractResults(dataArr2)

    else:
        print("NOT FOUND", API_LIST)
        dataArr2 = ["N/A","no","low"]
        extractResults(dataArr2)


def amsiCheck():
    pe2 = pefile.PE("C:\Windows\System32\\amsi.dll")

    for section in pe2.sections:
        print(section.Name, "Virtual Address: ", hex(section.VirtualAddress), "Virtual Size: ",  hex(section.Misc_VirtualSize),
                    "Raw data size: ", section.SizeOfRawData )

    byt3s = []
    byt3s = pe2.sections[0].get_data() #read .text section append to byt3s 
    hash = hashlib.sha256()
    hash.update(byt3s)
    fHash = hash.hexdigest()
    print("hash is: {0}".format(fHash))
    
    i = 0
    while(i<20):
        hash = hashlib.sha256()
        byt3s = pe2.sections[0].get_data() #read .text section append to byt3s 
        hash.update(byt3s)
        fHash2 = hash.hexdigest()
        
        if fHash!=fHash2:
            x = logger.alert("Memory Patching Detected! ")
            dataArr = [x,"yes","high"] 
            extractResults(dataArr)
            i = i + 1
            break
        else:
            print("Continuing. ")
            i = i + 1
            if (i == 20):
                dataArr = ["Hash Not Changed","no","low"] 
                extractResults(dataArr)
        time.sleep(5)
    # ---------------------------


def main():
    
    #Define Threads
    th = threading.Thread(target=APIPull())
    th2 = threading.Thread(target=amsiCheck())
    
    # Start threads
    th.start()
    th2.start()

    # Wait for threads to finish
    th.join()
    th2.join()
    # --------------------------

if __name__ == "__main__":
    main()