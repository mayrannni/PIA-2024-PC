#!/bin/bash

#Functions
ports_scan() {
    read -p ">>Enter the range of ports youu want to scan (Example 1-100 or only one like 22): " ports
    read -p ">>Enter the IP to scan: " IP #The IP has the following format ***.***.***.*** 0-255
    read -p ">>Enter the name of the file where yout results will be saved (just the file name not the path): " file
    #check that the file ends in .txt if not added
    if [[ $file =~ \.txt*$ ]]; then
        file=$file
    else
        file="$file.txt"
    fi
    path="$PWD/$file"
    errors="$PWD/errorsPortScan.log"
    #Create a new file
    touch $path
    #Extract open ports from a given IP
    nmap -p $ports $IP > $path 2> $errors
    if [[ -s $errors ]];then
        echo "We have an errors wich are saved in: $errors"
    else
        rm $errors
        echo "The port scan has completed and the file has been saved to: $path"
    fi
}

vulnerability_scan() {
    read -p ">>Enter the IP to scan: " IP #The IP has the following format ***.***.***.*** 0-255
    read -p ">>Enter the name of the file where yout results will be saved (please include .txt termination): " file
    #check that the file ends in .txt if not added
    if [[ $file =~ \.txt*$ ]]; then
        file=$file
    else
        file="$file.txt"
    fi
    path="$PWD/$file"
    pathScan="$PWD/test.txt"
    errorsV="$PWD/errorsVuln.log"
    #Create a new file
    touch $pathScan
    #Chek open ports and extract vulnerabilities
    nmap -p $ports $IP | grep 'open' > $pathScan 2> $errorsV
    if [[ -s $errorsV ]];then
        echo "We have an errors wich are saved in: $errors"
    else
        rm $errorsV
        if [[ -s $pathScan ]];then
            touch $path
            nmap -sV --script=vuln $IP > $path 2> $errorsV
            if [-s $errorsV];then
                echo "We have an errors wich are saved in: $errorsV"
            else
                rm $errorsV
                rm $pathScan
                echo "The port scan has completed and the file has been saved to: $path"
            fi
        else
            echo "The scan did not run because there are no ports open"
        fi
    fi
}

option=0
#Menu
while [[ $option -ne 3 ]]; do
    echo "===== Welcome to the Scanner ====="
    echo "Select the option:"
    echo "1. Scan ports"
    echo "2. Scan vulnerabilities"
    echo "3. Exit"
    echo "==== ==== ==== ==== ==== ==== ===="
    read -p ">>Enter your option: " option

    case $option in
        1) ports_scan ;;
        2) vulnerability_scan ;;
        3) echo "See you soon :D" ;;
        *) echo "Invalid option try again" ;;
    esac
done
