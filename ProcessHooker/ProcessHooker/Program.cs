﻿using System;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Management;
using System.Collections.Generic;
using System.IO;
using detection;
using System.Security.Cryptography;
using System.Text;
using CsvHelper;
using System.Globalization;
using CsvHelper.Configuration;

namespace ProcessHooker
{
    class Hook
    {
        public struct MODULEINFO
        {
            public IntPtr lpBaseOfDll;
            public uint SizeOfImage;
            public IntPtr EntryPoint;
        }


        //implement required kernel32.dll functions 

        [DllImport("kernel32")]
        public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);

        [DllImport("kernel32")]
        public static extern IntPtr CloseHandle(IntPtr hObject);

        [DllImport("kernel32.dll")]
        public static extern bool WriteProcessMemory(int hProcess, int lpBaseAddress, byte lpBuffer, int nSize, int lpNumberOfBytesWritten);

        [DllImport("kernel32.dll")]
        public static extern bool ReadProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, int dwSize, ref int lpNumberOfBytesRead);

        [DllImport("psapi.dll", SetLastError = true)]
        public static extern bool GetModuleInformation(IntPtr hProcess, IntPtr hModule, out MODULEINFO lpmodinfo, uint cb);

        [DllImport("psapi.dll")]
        static extern uint GetModuleHandleEx(IntPtr hProcess, IntPtr lpModuleName, IntPtr hModule);

        [DllImport("psapi.dll", SetLastError = true)]
        public static extern bool EnumProcessModules(IntPtr hProcess, [Out] IntPtr lphModule, UInt32 cb, [MarshalAs(UnmanagedType.U4)] out UInt32 lpcbNeeded);

        [DllImport("psapi.dll")]
        static extern uint GetModuleFileNameEx(IntPtr hProcess, IntPtr hModule, [Out] StringBuilder lpBaseName, [In][MarshalAs(UnmanagedType.U4)] int nSize);


        static void csvWriter(Data grabData, Data grabDiskData) //recieves object (Data is the class and grabData is the object name)
        {


            var dataList = new List<Data>
            {
                new Data{ Action = grabData.Action, Priority = grabData.Priority, Label = grabData.Label, EntryPoint = grabData.EntryPoint,
                    VirtualMemorySize = grabData.VirtualMemorySize, RawDataSize = grabData.RawDataSize, Hash = grabData.Hash, HashState = grabData.HashState},

                new Data{ Action = grabDiskData.Action, Priority = grabDiskData.Priority, Label = grabDiskData.Label, EntryPoint = grabDiskData.EntryPoint,
                    VirtualMemorySize = grabDiskData.VirtualMemorySize, RawDataSize = grabDiskData.RawDataSize, Hash = grabDiskData.Hash, HashState = grabDiskData.HashState}
            };
            



            if (File.Exists(MyStaticValues.DataFile))
            {
               
                using (var stream = File.Open(MyStaticValues.DataFile, FileMode.Append))
                using (var writer = new StreamWriter(stream))
                using (var csvWriter = new CsvWriter(writer, CultureInfo.InvariantCulture))
                {
                    foreach (Data d in dataList)
                    {
                        csvWriter.WriteRecord<Data>(d);
                    }
                }
            }
            
              else
             {
                File.Create(MyStaticValues.DataFile);
                //using (var stream = File.Open(MyStaticValues.DataFile))
                //using (var writer = new StreamWriter(stream))
                using (StreamWriter sw = new StreamWriter(MyStaticValues.DataFile))
                using (var csvWriter = new CsvWriter(sw, CultureInfo.InvariantCulture))
                {
                    csvWriter.WriteHeader<Data>();
                    foreach (Data d in dataList)
                    {
                        csvWriter.WriteRecord<Data>(d);
                    }
                }
            }
             
        }


        static void startWatch_EventArrived(object sender, EventArrivedEventArgs e)
        {
            //Console.WriteLine("[+] EventArrived function");
            string processName = (string)e.NewEvent.Properties["ProcessName"].Value;
            if (string.Equals(processName, "powershell.exe"))
            {
                Console.WriteLine("New PowerShell process started: ");

                Process[] processlist = Process.GetProcessesByName("powershell");
                foreach (Process p in processlist)
                {
                    Console.WriteLine("Process Name: {0} \tProcess ID: {1}", p.ProcessName, p.Id);
                }

                OnDiskAnalyzer(processlist[0].Id); //hook into the new powershell process for monitoring

            }



        }
        /*
        static void IntegrityCheck(int pid)
        {
            Console.WriteLine("[+] IntegrityCheck called");

            int PROCESS_ALL_ACCESS = (0x1F0FFF);
            IntPtr myHandle = OpenProcess(PROCESS_ALL_ACCESS, true, pid); //Handle to new PowerShell process

            if (myHandle == null)
            {
                Console.WriteLine("[-] Couldn't open handle");
                System.Environment.Exit(0);
            }
            //int i = 0;
            //while (i < 10) {
            //string onDiskHash = OnDiskAnalyzer();
            //string inMemoryHash = InMemoryAnalyzer(myHandle);

            //Console.WriteLine("[INFO] On Disk: {0} \n[INFO] In memory: {1}", onDiskHash, inMemoryHash);

            
            if (inMemoryHash.Equals(onDiskHash) == false)
            {
                Console.WriteLine("[+] Memory Patching Detected in process: {0}", pid);

                Data grabData = new Data();
                grabData.Action = 1;
                grabData.Priority = "High";
               
                //write data to csv including hash in numeric terms, entry point for process, raw data size, etc
                csvWriter(grabData);
                
                CloseHandle(myHandle);
            }
            else
            {
                Console.WriteLine("[+] Process has not been tampered with: {0}", pid);
                Data grabData = new Data();
                grabData.Action = 0;
                grabData.Priority = "Low";

                //write data to csv including hash in numeric terms, entry point for process, raw data size, etc
                csvWriter(grabData);
                CloseHandle(myHandle);

            }
            
            
        }
            */
        static string OnDiskAnalyzer(int pid)
        {
            Console.WriteLine("[+] Disk analyzer called");

            int PROCESS_ALL_ACCESS = (0x1F0FFF);
            IntPtr myHandle = OpenProcess(PROCESS_ALL_ACCESS, true, pid); //Handle to new PowerShell process

            if (myHandle == null)
            {
                Console.WriteLine("[-] Couldn't open handle");
                System.Environment.Exit(0);
            }

            PeHeaderReader onDiskAmsiReader = new PeHeaderReader("C:/Windows/System32/amsi.dll");
            PeHeaderReader.IMAGE_SECTION_HEADER[] onDiskAmsiSection = onDiskAmsiReader.ImageSectionHeaders;
            byte[] onDiskAmsi = onDiskAmsiReader.allBytes; //read entire string of bytes of amsi file

            int i;

            for (i = 0;i < onDiskAmsiSection.Length; i++)
                { 
                char[] headerName = onDiskAmsiSection[i].Name; //grabbing char value and storing it into char array so we can reference it

                if (headerName[0] == '.' && headerName[1] == 't' && headerName[2] == 'e' && headerName[3] == 'x' && headerName[4] == 't')
                    {
                    int RawData = (int)onDiskAmsiSection[i].PointerToRawData; // PointerToRawData is offset from the file's beginning to the section's data
                    int SizeOfRawData = (int)onDiskAmsiSection[i].SizeOfRawData;
                    int VirtualMemorySize = (int)onDiskAmsiSection[i].VirtualSize;
                    int EntryPoint = (int)onDiskAmsiSection[i].VirtualAddress;
                    byte[] onDiskAmsiCodeSection = new byte[SizeOfRawData];
                    Array.Copy(onDiskAmsi, RawData, onDiskAmsiCodeSection, 0, SizeOfRawData); //copy ondiskAmsi and rawdata into ondiskamsicodesection array up to sizeofrawdata
                    string AmsiHash = calculateHash(onDiskAmsiCodeSection); // md5 Hash of ondisk Amsi.dll

                    //int numericHash = AmsiHash -> numeric value;
                    //long numericHash = Convert.ToInt64(AmsiHash, 16); //ulong.Parse(AmsiHash, System.Globalization.NumberStyles.HexNumber);

                    
                    Data grabDiskData = new Data();
                    grabDiskData.RawDataSize = SizeOfRawData;
                    //grabDiskData.Hash = numericHash;
                    grabDiskData.EntryPoint = EntryPoint;
                    grabDiskData.VirtualMemorySize = VirtualMemorySize;

                    InMemoryAnalyzer(pid, myHandle, grabDiskData, AmsiHash);

                    return AmsiHash;
                    }
                }
            return "[-] Error: .text SECTION NOT FOUND";
        }




        static IntPtr AmsiHandleOpener(IntPtr myHandle)
        {
            // Credit to Aden Chung Wee Jing (https://github.com/countercept/AMSIDetection/tree/14418b3a236b85269048069f94d15887f6afbbb8) for help in this section
            Console.WriteLine("[+] AMSI Handler function opened ");
            IntPtr[] listOfModules = new IntPtr[1024]; //define list to store modules handles for use in EnumProcessModules
            GCHandle gch = GCHandle.Alloc(listOfModules, GCHandleType.Pinned); //using GCHandle to create a managed object (array) in unmanaged space to prevent grabage collector from freeing before use
            IntPtr modulePointer = gch.AddrOfPinnedObject(); //pointer to array
            uint arrSize = (uint)(Marshal.SizeOf(typeof(IntPtr)) * (listOfModules.Length)); // calculate size of array in bytes
            uint bytesNeeded = 0;

            //if statement seems to fail so not handle is being opened for module (amsi in memory) therefore no hash is found
           if (EnumProcessModules(myHandle, modulePointer, arrSize, out bytesNeeded)) //returns non zero if it succeeds, retreieve a handle for each module in the specified process (powershell)
            {
                int numOfModules = (Int32)(bytesNeeded / (Marshal.SizeOf(typeof(IntPtr)))); // number of modules from bytes to characters in the list
                for (int x = 0; x <= numOfModules; x++)
                {
                    StringBuilder moduleName = new StringBuilder(1024); // why is string builder needed here? Memory access violation if i use a normal string array ----------------------------------
                    GetModuleFileNameEx(myHandle, listOfModules[x], moduleName, (int)(moduleName.Capacity)); //retreives path for the file
                    //Console.WriteLine("ListOfModules = {0} \nmoduleName = {1}", listOfModules[x], moduleName);
                    if (moduleName.ToString().Contains("amsi.dll"))
                    {
                        //InMemoryAnalyzer(myHandle, listOfModules[x]);
                        gch.Free();
                        Console.WriteLine("[+] Found amsi.dll in memory");
                        return listOfModules[x];
                    }
                    
                }
            }
            gch.Free();
            Console.WriteLine("[-] Couldn't open handle");
            return IntPtr.Zero;
            System.Environment.Exit(0);

        }
        static string InMemoryAnalyzer(int pid, IntPtr myHandle,Data grabDiskData, string onDiskAmsiHash)
        {
            Console.WriteLine("[+] Memory analyzer called");

            int bytesRead = 0;
            MODULEINFO amsiDLLInfo = new MODULEINFO(); //creates an object of the moduleinfo structure
        
            IntPtr amsiModuleHandle = AmsiHandleOpener(myHandle);
            

            GetModuleInformation(myHandle, amsiModuleHandle, out amsiDLLInfo, (uint)Marshal.SizeOf(typeof(MODULEINFO))); //Get info of the current hooked module from the hooked process, like entry point, size of image etc and store in MODULEINFO structure
            byte[] InMemoryAmsi = new byte[amsiDLLInfo.SizeOfImage]; //defines a byte array to be size of the image.
            ReadProcessMemory(myHandle, amsiModuleHandle, InMemoryAmsi, InMemoryAmsi.Length, ref bytesRead); // copies the information of the hooked module to InMemoryAmsi buffer
            
            PeHeaderReader InMemoryAmsiReader = new PeHeaderReader(InMemoryAmsi); //read the bytes copied from the in memory amsi dll
            PeHeaderReader.IMAGE_SECTION_HEADER[] InMemoryAmsiSection = InMemoryAmsiReader.ImageSectionHeaders; //grab headers of this in memory amsi dll
            int i;

            for (i = 0; i < InMemoryAmsiSection.Length; i++)
            {
                char[] headerName = InMemoryAmsiSection[i].Name; //grabbing char value and storing it into char array so we can reference it
                if (headerName[0] == '.' && headerName[1] == 't' && headerName[2] == 'e' && headerName[3] == 'x' && headerName[4] == 't') // grab .text header for in memory amsi dll
                    {
                    int VirtualAddr = (int)InMemoryAmsiSection[i].VirtualAddress; // .VirtualAddress is known attribute in c#
                    int SizeOfRawData = (int)InMemoryAmsiSection[i].SizeOfRawData;
                    int VirtualMemorySize = (int)InMemoryAmsiSection[i].VirtualSize;
                    
                    byte[] InMemoryAmsiCodeSection = new byte[SizeOfRawData];
                    Array.Copy(InMemoryAmsi, VirtualAddr, InMemoryAmsiCodeSection, 0, SizeOfRawData); //copy 
                    string inMemoryAmsiHash = calculateHash(InMemoryAmsiCodeSection); // md5 Hash of ondisk Amsi.dll

                    //int numericHash = AmsiHash -> numeric value;
                    //long numericHash = Convert.ToInt64(AmsiHash, 16);//ulong.Parse(AmsiHash, System.Globalization.NumberStyles.HexNumber);

                    if (inMemoryAmsiHash.Equals(onDiskAmsiHash) == false)
                    {
                        Console.WriteLine("[+] Memory Patching Detected in process: {0}", pid);

                        Data grabData = new Data();
                        grabData.Action = 1;
                        grabData.Priority = "High";
                        grabData.RawDataSize = SizeOfRawData;
                        //grabData.Hash = numericHash;
                        grabData.EntryPoint = VirtualAddr;
                        grabData.VirtualMemorySize = VirtualMemorySize;
                        grabData.HashState = 1;
                        grabDiskData.Action = 1;
                        grabDiskData.Priority = "High";
                        grabDiskData.HashState = 1;

                        //write data to csv including hash in numeric terms, entry point for process, raw data size, etc
                        csvWriter(grabData, grabDiskData);

                        CloseHandle(myHandle);
                    }
                    else
                    {
                        Console.WriteLine("[+] Process has not been tampered with: {0}", pid);
                        Data grabData = new Data();
                        grabData.Action = 0;
                        grabData.Priority = "Low";
                        grabData.RawDataSize = SizeOfRawData;
                        //grabData.Hash = numericHash;
                        grabData.EntryPoint = VirtualAddr;
                        grabData.VirtualMemorySize = VirtualMemorySize;
                        grabData.HashState = 0;
                        grabDiskData.Action = 0;
                        grabDiskData.Priority = "Low";
                        grabDiskData.HashState = 0;

                        //write data to csv including hash in numeric terms, entry point for process, raw data size, etc
                        csvWriter(grabData, grabDiskData);
                        CloseHandle(myHandle);

                    }


                    return inMemoryAmsiHash;
                }
            }
            return "[-] Error: .text SECTION NOT FOUND";
        }





        static String calculateHash(byte[] bytesToHash) //takes byte array (and calls it bytesToHash) to hash (from Analyzer functions)
        {
            MD5 md5CheckSum = MD5.Create();
            var hash = md5CheckSum.ComputeHash(bytesToHash);
            return BitConverter.ToString(hash).Replace("-", "").ToLowerInvariant();
        }




        static void Main(string[] args)
        {
            Console.WriteLine("Is this a malicious program? Yes = 1 No = 0");
            string Label = Console.ReadLine();

            Data grabData = new Data();
            grabData.Label = Label;

            ManagementEventWatcher watcher = new ManagementEventWatcher(new WqlEventQuery("SELECT * FROM Win32_ProcessStartTrace"));

            watcher.EventArrived += new EventArrivedEventHandler(startWatch_EventArrived);
            watcher.Start();

            Console.WriteLine("Press any key to exit");
            while (!Console.KeyAvailable) System.Threading.Thread.Sleep(50);
            watcher.Stop();



        }

        
    
    }

    public static class MyStaticValues
    {
        public static string DataFile = "C:/Users/Dev1/Documents/Dataset5.csv";
    }

    public class Data
    {
        public int Action { get; set; }
        public string Priority { get; set; }
        public string Label { get; set; }
        public int EntryPoint { get; set; }
        public int VirtualMemorySize { get; set; }
        public int RawDataSize { get; set; }
        public long Hash { get; set; }
        public int HashState { get; set; }

    }

    


}