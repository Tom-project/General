import pefile
import os
import struct
import logging
import hashlib
import time
import threading
import csv
import datetime
#import pandas as pd

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

MalIdentifier = int(input("Is this run using a malicious program? 1 = Yes, 0 = No "))


def extractResults(df, df2): 
    #df["Data"] = df[0]
    #df["Action"] = df[1]
    #df["Priority"] = df[2]
    #df2.to_csv(r'C:\\Users\\thoma\Documents\dataset.csv', index=True)
    #df.to_csv(r'C:\\Users\\thoma\Documents\dataset.csv', index=False)

    #header = ['Data', 'Action', 'Priority', 'Malicious'] # Only needed when in write mode to create a new file
    data =[
            [df[0],df[1],df[2],df[3]],
            [df2[0],df2[1],df2[2],df[3]]
          ]
    with open(r"C:\Users\\thoma\Documents\dataset.csv", "a") as f: 
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        #writer.writerow(header)
        writer.writerows(data)
    



def APIPull():
    print("API Pull is running at time: " + str(int(time.time())) + " seconds.")
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

    i = 0
    while(i < 20):
        
        if ("GetProcAddress" in API_LIST): # Looking for Win API call of interest
            #print("GetProcAddress Found")
            x = API_LIST.index("GetProcAddress")
            logger.info(API_LIST[x])
            #b = input("Would you like to see the rest of the list? ")
            #if b == "y":
                #print(API_LIST)
            global df 
            df = [API_LIST[x],"1","medium",MalIdentifier]
            break
            

        else:
            i = i + 1
            if (i == 20):
                print("NOT FOUND", API_LIST)
                df = ["N/A","0","low",MalIdentifier]
        time.sleep(5)
            


def amsiCheck():
    print("AMSI Check is running at time: " + str(int(time.time())) + " seconds.")
     
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
    while(i<3):
        hash = hashlib.sha256()
        byt3s = pe2.sections[0].get_data() #read .text section append to byt3s 
        hash.update(byt3s)
        fHash2 = hash.hexdigest()
        
        if fHash!=fHash2:
            x = logger.alert("Memory Patching Detected! ")
            df2 = [x,"1","high"] 
            extractResults(df, df2)
            break
        else:
            print("Continuing. ")
            i = i + 1
            if (i == 2):
                df2 = ["Hash Not Changed","0","low"] 
                extractResults(df, df2)
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