name = input("Enter your name: ") #Takes user input for their name
ID = input("Enter your student ID: ") #declares a variable called ID
LengthName=len(name)#fidns length of user input name and declares a new variable
value = 0 #declares a variable with the value of 0
for i in ID:
    if int(i) > 2 and int(i) < 7: #checks to see if an integer in ID is between 2 and 7
        value = int(i) #if it is between 2 and 7 it assigns it to value
        break
if value == 0: #if there are no integers in ID between 2 and 7 it assumes it is 4
    value = 4


for i in range(1, len(name)+1):
    if name[i-1]==" ": #if there is a space character in the name then
        print(":", end="")#replace it with a smei colon
    else:
        if name[i-1].isupper():#checks if a character in name is an uppercase
            print(name[i-1].lower(), end="")#if it is turn it to a lower case

        else:
            print(name[i-1].upper(), end="")# if its a lower case then turn it to an upper case

    if i % value == 0:
        print("\n")#prints newline if the remainer of i mod value is 0


if (LengthName % value):
    padding = value - (LengthName % value)
    print("="*padding, end="") #if the name cant fill the value size then fill the gaps with a "=" symbol
