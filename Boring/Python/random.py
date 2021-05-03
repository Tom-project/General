import random

print("Enter the number of frames: ", end="")
capacity = int(input())  # User input for number of table entries

f, fault, pf = [], 0, 'No'  # defining variables

print("Enter the reference string: ", end="")
s = list(map(int, input().strip().split()))  # Takes a list of numbers/ proccesses needed to be fetched and executed.

print("\nString|Frame →\t", end='')  # Puts the number of tables enteries onto the same line


for i in range(capacity):
    print(i, end=' ') #This just formats the title "0 1 2 3 Fault"
print("Fault\n   ↓\n")
for i in s:
    if i not in f:
        if len(f) < (capacity): #checks if there is length to append to the end or not
            f.append(i)
        else:
            random_value = random.randrange(0, capacity - 1, 1) #Generates random value within specified range
            f[random_value] = i  # takes a random generated number and goes to that position in f and replcaes the value in that current position with i
        fault += 1
        pf = 'Yes'
    else:
        pf = 'No'
    print("   %d\t\t" % i, end='')
    for x in f:
        print(x, end=' ')
    for x in range(capacity - len(f)):
        print(' ', end=' ')
    print(" %s" % pf)
print("\nTotal requests: %d\nTotal Page Faults: %d\nFault Rate: %0.2f%%" % (len(s), fault, (fault / len(s)) * 100))
