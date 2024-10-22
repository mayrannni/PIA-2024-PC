"""Analyzes vulnerabilities that may exist in the target."""


import argparse
import datetime
import logging
import os
import re
import subprocess
import webbrowser
from menu import main_menu

def validate_ip(ip):
    """Validate a single IP."""
    pattern = re.compile(
        r"^"
        r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        r"$"
        )
    if pattern.match(ip):
        return ip
    else:
        raise argparse.ArgumentTypeError(
            'The IP address given is invalid.'
            )
    return ip


def validate_port(ports):
    """Validate port(s)"""
    if re.fullmatch(r'\d{1,5}', ports):
        port = int(ports)
        if 1 <= port <= 65535:
            return ports
        else:
            raise argparse.ArgumentTypeError(
                'The port is not within range'
                )
    if re.fullmatch(r'\d{1,5}-\d{1,5}', ports):
            beginning, end = map(int, ports.split('-'))
            if 1 <= beginning <=65535 and 1 <= end <= 65535 and beginning < end:
                return ports
            else:
                raise argparse.ArgumentTypeError(
                    'Ports are not within range'
                    )


def vulnerability_scanning(param):
    """Return the target's vulnerabilities."""
    try:
        command = ['nmap', '-p', param.ports, '--open', '-Pn',
                   '-T4', '-sV', '--script',
                   'vuln', param.ip]
        ps_line = 'powershell -Executionpolicy Bypass -Command ' + \
                  ' '.join(command)
        results = subprocess.run(ps_line, capture_output=True, text=True)
        logging.info(command)
        logging.info(ps_line)
        logging.info('Starting the process')
        if results.returncode == 0:
            if results:
                logging.info('The nmap scan has completed successfully.')
                with open(f'{name}', 'a') as file:
                    file.write(f'{results.stdout}')
                    logging.info(
                        f'The file has been successfully saved in: {name}.'
                        )
            else:
                logging.info('No known vulnerabilities were found.')
    except subprocess.CalledProcessError as e:
        logging.error(
            f'An error occurred while trying to execute the command: {e}'
            )
    except Exception as e:
        logging.error(f'An unexpected error has occurred: {e}')


mode = """Run the following command:
python "IPVulnerabilities.py" -ip -ports

Ideal scenario
- Install nmap from https://nmap.org/download

Notes
- This script requires nmap to be installed on your computer (https://nmap.org/download)
- The scan usually takes a while to complete"""
parser = argparse.ArgumentParser(
    description='The script scans an IP for its vulnerabilities using nmap.',
    epilog=mode,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-ip', dest='ip', help='Ip to be analyzed',
                    type=validate_ip, required=True)
parser.add_argument('-ports', dest='ports', type=validate_port,
                    help='Port to be analyzed', required=True)
param = parser.parse_args()


date = datetime.datetime.now()
name = r'VulnerabilityScanning_'
name += str(date.strftime('%Y%m%d_%H%M%S'))
name += '.txt'

info = r'scanner'
info += str(date.strftime('%Y%m%d_%H%M%S'))
info += '.log'

logging.basicConfig(filename=f'{info}', level=logging.INFO)
logging.info(os.path.join(os.getcwd(), name))


try:
    logging.info('Checking if nmap is installed.')
    result = subprocess.run(['Nmap', '--version'],
                            check=True, capture_output=True, text=True)
    nmap_exist = 'True'
except (subprocess.CalledProcessError, FileNotFoundError):
    logging.info('nmap is not installed, redirecting to download page')
    install = webbrowser.open('https://nmap.org/download')
    logging.info(install)
    nmap_exist = 'False'


if nmap_exist == 'True':
    logging.info('Nmap is installed')
    vulnerability_scanning(param)

main_menu()
