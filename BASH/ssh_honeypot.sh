#!/bin/bash

port=22
report="$HOME/ssh_attempts.log"

#create honeypot function
create_honeypot() {
    #need this number to avoid saturating the processes
    read -p ">> how many times do you want to listen ssh connections? " connections
    i=0
    sleep 2s
    echo "building up honeypot at 22 port..."
    #search os information for banner to attract access attempts
    os_name=$(lsb_release -d | awk -F'\t' '{print $2}') #e.g. Kali GNU/Linux Rolling
    kernel_ver=$(uname -r) #e.g. 6.6.9-amd64
    ssh_ver=$(ssh -V 2>&1 | awk '{print $1}') #e.g. OpenSSH_9.6p1

    banner="SSH-2.0-$ssh_ver $os_name $kernel_ver"

    while [ $i -lt $connections ]; do
        #fooling with my banner, try to listen 22 port using netcat
        echo -e "$banner" | nc -lvp $port
        #filter netstat results that we are interested and extract the ip
        found_ip=$(netstat -tnp 2>/dev/null | grep ":$port " | grep "ESTABLISHED" | awk '{print $5}' | cut -d: -f1)
        if [ -n "$found_ip" ]; then
            #if ip was detected then save the following msg in a log file (report)
            echo "ssh access attempt from ip: $found_ip === $(date)" >> $report
        fi
        echo "ITERATION $i"
        ((i++))
    done
}

show_report() {
    if [ -f "$report" ]; then
        echo "showing $report"
        cat $report
    else
        echo "report not found :("
    fi
}

exit_script() {
    echo "stopping honeypot..."
    sleep 3s
    #kill process strictly called "nc -lvp" (our honeypot basically)
    pkill -f "nc -lvp"
    echo "ssh honeypot has stopped, goodbye!"
    exit 0
}
#menu
while true; do
    echo "=== welcome to ssh honeypot ==="
    echo "1) start"
    echo "2) view results"
    echo "3) exit"
    echo "=== === === === === === === ==="
    read -p ">> your choice: " choice

    case $choice in
        1) create_honeypot ;;
        2) show_report ;;
        3) exit_script ;;
        *) echo "your choice must be between 1 and 3, please try again" ;;
    esac
done
