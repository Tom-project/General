a = []

# Function to accept reference string and frame size.


def accept():
    m = 4
    n = 0
    for i in range(n):
        a.append(input(" Enter [%2d] : " % (i + 1)))
    

# First In First Out Page Replacement Algorithm


def __fifo():
    f = -1
    page_faults = 0
    page = []
    for i in range(m):
        page.append(-1)

    for i in range(n):
        flag = 0
        for j in range(m):
            if(page[j] == a[i]):
                flag = 1
                break

        if flag == 0:
            f = (f + 1) % m
            page[f] = a[i]
            page_faults += 1
            print("\n%d ->") % (a[i]),
            for j in range(m):
                if page[j] != -1:
                    print (page[j]),
                else:
                    print ("-"),
        else:
            print ("\n%d -> No Page Fault") % (a[i]),

    print ("\n Total page faults : %d.") % (page_faults)


accept()
__fifo()
