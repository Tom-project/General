print("Enter the number of frames: ", end="")
capacity = int(input())  # User input for number of table entries

f, fault, top, pf = [], 0, 0, 'No'  # defining variables

print("Enter the reference string: ", end="")
s = list(map(int, input().strip().split()))  # Takes a list of numbers/ proccesses needed to be fetched and executed.

print("\nString|Frame →\t", end='')  # Puts the number of tables enteries onto the same line as the the "String|Frame" string


for i in range(capacity):  # Counts down from the capacity number
    print(i, end=' ')  # Prints the integer and positions it
print("Fault\n   ↓\n")
for i in s:
    if i not in f:  # Checks to see if the next integer in the list is already in the array
        if len(f) < capacity:  # if array has less numbers than the capacity allowed
            f.append(i)  # Then append the next integer onto the end of the array
        else:
            f[top] = i
            top = (top + 1) % capacity
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
