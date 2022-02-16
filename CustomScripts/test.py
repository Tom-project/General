import psutil

def main():
   
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            #print(processName , ' ::: ', processID)

            if (processName == "powershell.exe"):
                #print(processID)
                pshell = processID
                return pshell
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def test():
    pshell = main()
    print(pshell)

  

main()
test()