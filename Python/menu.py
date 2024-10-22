"""Do the scripts management"""

import sys
import subprocess
import time
import re


def input_help_validator(help_command):
    """Validate help command"""
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        try:
            get_help = input(
                "You want to see the script help first? (Recommended): y/n >> "
            )
            show_help = get_help.strip().lower()
            if show_help == "y":
                print("SHOWING HELP ========== :)")
                time.sleep(3)
                try:
                    subprocess.run(help_command, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Sorry, error when showing help. (Error: {e}) ")
                break
            elif show_help == "n":
                print("Continuing without showing help...")
                time.sleep(3)
                break
            else:
                raise ValueError("Unable to process your input.")
        except ValueError as e:
            attempts += 1
            print(f"{e}. {max_attempts - attempts} attemp(s) remaining.")

    if attempts == max_attempts:
        print("Too many incorrect attempts.")
        print("Continuing without displaying help.")
        time.sleep(3)


def main_menu():
    """Show menu for manage scripts"""
    print("Cybersecutiry Tasks in Python")
    print("1. Scan vulnerabilities for websites")
    print("2. Check open ports - SHODAN")
    print("3. Use IP Abuse Database")
    print("4. Scanning IP addreses - NMAP")
    print("5. Reporting IP addresses")
    print("6. Exit")

    choice = input("Select a cybersecurity function to start >> ")

    if choice == "1":
        help_command = ["python", "web_scanning.py", "--help"]
        input_help_validator(help_command)
        print("-----------------------------------------------------------")
        print("SCAN VULNERABILITIES FOR WEBSITES")

        # validating script option 1 parameters
        url_regex = re.compile(
            r"^(https?:\/\/)?"
            r"([a-zA-Z0-9.-]+)"
            r"(\.[a-zA-Z]{2,6})"
            r"(:[0-9]{1,5})?"
            r"(\/.*)?$"
        )
        apikey_regex = re.compile(r"^[a-zA-Z0-9]{20,40}$")

        while True:
            url_msg = "Enter the url to scan (e.g. 'https://example.com'): "
            apikey_msg = "API-KEY (e.g. 'jfacsqm6agh97lf49l923tch46'): "
            target_url = input(url_msg)
            zapikey = input(apikey_msg)
            if url_regex.match(target_url) and apikey_regex.match(zapikey):
                break
            else:
                print("Some parameters are inapplicable. Try again.")
                time.sleep(1)

        subprocess.run(
            ["python", "web_scanning.py", "-url", target_url, "-zapikey", zapikey]
        )  # run web scanning

    elif choice == "2":
        help_command = ["python", "open_ports.py", "--help"]
        input_help_validator(help_command)
        print("-----------------------------------------------------------")
        print("VERIFY OPEN PORTS WITH SHODAN")

        ip = input("Enter the IP to scan (e.g. '8.8.8.8'): ")
        subprocess.run(["python", "open_ports.py", "-ip", ip])

    elif choice == "3":
        help_command = ["python", "ip_inspector.py", "--help"]
        input_help_validator(help_command)
        print("-----------------------------------------------------------")
        print("INFORMATION FROM IP ABUSE DATABASE")

        ip_to_scan = input("Enter the IP to scan: ")
        day = input("Enter a day from 1 to 365: ")
        trust = input("Confidence limit from 25 to 100: ")
        ip_range = input("Interested IP range (e.g. /24): ")
        subprocess.run(
            [
                "python",
                "ip_inspector.py",
                "-ip",
                ip_to_scan,
                "-day",
                day,
                "-trust",
                trust,
                "-ip_range",
                ip_range,
            ]
        )

    elif choice == "4":
        help_command = ["python", "ip_scanning.py", "--help"]
        input_help_validator(help_command)
        print("-----------------------------------------------------------")
        print("SCANNING IP ADDRESSES WITH NMAP")

        ip_nmap = input("Enter the IP to scan with nmap: ")
        ports_range = input("Enter port/range ports (e.g. 80 or 25-30): ")
        subprocess.run(
            ["python", "ip_scanning.py", "-ip", ip_nmap, "-ports", ports_range]
        )

    elif choice == "5":
        help_command = ["python", "report_ip.py", "--help"]
        input_help_validator(help_command)
        print("-----------------------------------------------------------")
        print("REPORT AN IP WITH IP ABUSE DB")

        file_path = input("Enter the file NMAP scan path: ")
        subprocess.run(["python", "report_ip.py", "-file", file_path])

    elif choice == "6":
        sys.exit()

    else:
        print("Invalid option. Please try again.")
        main_menu()


if __name__ == "__main__":
    main_menu()
