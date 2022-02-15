using System;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Management;

namespace ProcessHooker
{
    class Hook 
    {
        //implement required kernel32.dll functions 
        [DllImport("kernel32")]
        public static extern IntPtr LoadLibrary(string name);
        [DllImport("kernel32")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

        [DllImport("kernel32")]
        public static extern IntPtr OpenProcess(int dwDesiredAccess,bool bInheritHandle,UInt32 dwProcessId);

        [DllImport("kernel32")]
        public static extern IntPtr CloseHandle(IntPtr hObject);

        [DllImport("kernel32.dll")]
        public static extern bool WriteProcessMemory(int hProcess, int lpBaseAddress, byte lpBuffer,
                                         int nSize, int lpNumberOfBytesWritten);

        
        /*
        [DllImport("kernel32")]
        public static extern bool VirtualProtect(IntPtr lpAddress, int dwSize, uint flNewProtect, out IntPtr lpflOldProtect);
        
        [DllImport("kernel32.dll", EntryPoint = "RtlMoveMemory", SetLastError = false)]
        static extern void MoveMemory(IntPtr dest, IntPtr src, int size);
        */
        static void csvchecker()
        {


        }

        int findPshellProcess()
        {
            Process[] processlist = Process.GetProcessesByName("powershell");

            foreach (Process p in processlist)
            {
                Console.WriteLine("Process: {0} ID: {1}", p.ProcessName, p.Id);
            }

            return processlist[0].Id;
        }

        void WaitForProcess()
        {
            ManagementEventWatcher startWatch = new ManagementEventWatcher(new WqlEventQuery("SELECT * FROM Win32_ProcessStartTrace"));
            
            startWatch.EventArrived += new EventArrivedEventHandler(startWatch_EventArrived);
            startWatch.Start();
        }

        static void startWatch_EventArrived(object sender, EventArrivedEventArgs e)
        {
            string processName = (string)e.NewEvent.Properties["ProcessName"].Value;
            if (string.Equals(processName, "powershell.exe"));
                {
                Console.WriteLine("New PowerShell process started: ");
                    startWatch.Stop();
                }
          
        }

        static void handlehooking()
        {
            Hook myProcess = new Hook(); //create object to get powerhsell pid

            myProcess.findPshellProcess();
            //int myProcess = findPshellProcess();
            int PROCESS_ALL_ACCESS = (0x1F0FFF);

            IntPtr myHandle = OpenProcess(PROCESS_ALL_ACCESS, false, myProcess); //Handle to new PowerShell process




            CloseHandle(myHandle);

        }

        static void sectionFinder()
        {
            PeHeaderReader onDiskAmsiReader = new PeHeaderReader("C:\Windows\System32\\amsi.dll");
            PeHeaderReader.IMAGE_SECTION_HEADER[] onDiskAmsiSection = onDiskAmsiReader.ImageSectionHeaders;

            if(onDiskAmsiSection[count].Equals(".text"))
            {
                int rawdata = (int)onDiskAmsiSection[count].rawdata;
                int sizeofrawdata = (int)onDiskAmsiSection[count].sizeofrawdata;
            }

            

        }

        static void Main(string[] args)
        {
            Console.WriteLine("Is this a malicious program? Yes = 1 No = 0");
            string Label = Console.ReadLine();
            
            handlehooking();

        }

        
    
    }
}