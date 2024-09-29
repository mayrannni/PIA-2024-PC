#!/bin/bash

# Functions
ports_scan() {
    read -p ">>Enter the range of ports you want to scan (Example 1-100 or only one like 22): " ports
    read -p ">>Enter the IP to scan: " IP # The IP has the following format ***.***.***.*** 0-255
    read -p ">>Enter the name of the file where your results will be saved (just the file name, not the path): " file
    # Check that the file ends in .txt if not added
    if [[ $file =~ \.txt*$ ]]; then
        file=$file
    else
        file="$file.txt"
    fi
    path="$PWD/$file"
    errors="$PWD/errorsPortScan.log"
    # Create a new file
    touch $path
    # Extract open ports from a given IP
    nmap -p $ports $IP > $path 2> $errors
    # Error manage
    if [[ -s $errors ]];then
        echo "We have errors which are saved in: $errors"
    else
        # If we have no error the error file will be removed
        rm $errors
        echo "The port scan has completed and the file has been saved to: $path"
    fi
}

vulnerability_scan() {
    read -p ">>Enter the IP to scan: " IP # The IP has the following format ***.***.***.*** 0-255
    read -p ">>Enter the name of the file where your results will be saved (please include .txt termination): " file
    # Check that the file ends in .txt if not added
    if [[ $file =~ \.txt*$ ]]; then
        file=$file
    else
        file="$file.txt"
    fi
    # Create the path for the port open Scan, vulnerabilities scan, and errors
    path="$PWD/$file"
    pathScan="$PWD/test.txt"
    errorsV="$PWD/errorsVuln.log"
    # Create a new file for the open ports scan
    touch $pathScan
    # Chek open ports and extract vulnerabilities
    nmap $IP | grep 'open' > $pathScan 2> $errorsV
    if [[ -s $errorsV ]];then
        echo "We have errors which are saved in: $errors"
    else
        # If the last command executes correctly the error.log file will be deleted 
        rm $errorsV
        # Reviewing the output from the open ports scan to check if there is at least one open port
        if [[ -s $pathScan ]];then
            # Create the vulnerabilites 
            touch $path
            # If we have at least one open port we do the nmap vulnerabilities scan
            nmap -sV --script=vuln $IP > $path 2> $errorsV
            if [ -s $errorsV ];then
                # The error manage
                echo "We have errors which are saved in: $errorsV"
            else
                # If there is no error in the vulnerabilities scan we remove the test ports open scan file and error file
                rm $errorsV
                rm $pathScan
                echo "The port scan has completed and the file has been saved in: $path"
            fi
        else
            # If the file of the open ports scan is empty (that means there are no open ports) the vulnerabilities scan will not realesed
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
