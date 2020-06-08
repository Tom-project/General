import subprocess

while True:
        user_input = int(input("Which process would you like to complete? \n 1. Display information about the cpus \n 2. Dsplay a list of device drivers configured into the currently running kernel\n 3. Display the load average of the system \n 4. Display the PID and PPID of a process \n 5. Exit\n Enter answer here:  "))

        if user_input == 1:
                print(subprocess.run("cat /proc/cpuinfo", shell=True))

        elif user_input == 2:
                print(subprocess.run("cat /proc/modules | wc -l", shell=True))

        elif user_input == 3:
                print(subprocess.run("cat /proc/loadavg", shell=True))

        elif user_input == 4:
                print(subprocess.run("cat /proc/ ps -efj | grep agetty"))

        elif user_input == 5:
                break

        else:
                print("Invalid Input")
