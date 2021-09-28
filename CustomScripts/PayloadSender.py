import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creating socket


Host = input("Enter the address of the host: ")
Port = int(input("Please specify the port: "))
payload = input("Enter your payload: ")


print("[+]Connecting to host...")
time.sleep(2)

try:
    s.connect((Host, Port)) #Checking to see if connection was successfull

except OSError as msg:
    s.close()
    s = None

if s is None:
    print("[-]Something went wrong. Please try again.")
else:
    print("[+]Connection successful...")
    time.sleep(1)
    print("[+]Sending payload...")
    s.sendall(str.encode(payload))
    data = s.recv(1024)

print('Recieved', repr(data)) #Receving data back

