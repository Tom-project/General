# Overview

A repo for all custom scripts for various vulnerabilities. 

## Bruteforce.sh
A shell script initially to bruteforce creds to gain authenticated RCE via a vulnerable Splunk application
> However, can be used to bruteforce creds for any authenticated rce exploit

## Payload sender/ Remote-BOF
Both of these are scripts to send malicious payloads remotely to exploit applications vulnerable to Buffer Overflows.

## Ret2Libc
A python script exploiting a vlnerable binary i used for privilege escalation via ret2libc.

## Upload
A script to upload a malicious plugin to a vulnerable moodle interface to achieve RCE

## Windows-Remote-BOF-Fuzzer
A python script to find EIP register on remote vulnerable applications.

## SQLBinarySearch
This is a script that uses the binary search algorithm to enumerate information from a server vulnerable to blind sql injection. This script will only work if there is some
 way to determine if a statement is true or false. For total blind sql injection see SQLBinaryTimebased

## SQLBinaryTimebased
This is a script that uses the binary search algorithm to enumerate information from a server vulnerable to blind sql injection via a time based attack.

## ExtractWin32APICalls.py
This extracts APIs from PE on a Windows machine.

## intOverflow.c
This is a exploit in c to target an application vulnerable to an integer overflow

## VectorizeData.py
A python script to pull API data and a hash of .text section of amsi.dll
