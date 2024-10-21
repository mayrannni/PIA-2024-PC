"""Analyzes vulnerabilities that may exist in the target."""


import datetime
import logging
import os
import subprocess
import argparse
import webbrowser


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


mode = '''How to use: python "IPVulnerabilities.py" -ip -ports '''
parser = argparse.ArgumentParser(
    description='The script scans an IP for its vulnerabilities using nmap.',
    epilog=mode,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-ip', dest='ip', help='Ip to be analyzed', required=True)
parser.add_argument('-ports', dest='ports',
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
    result = subprocess.run(['Nmap', '--version'],
                            check=True, capture_output=True, text=True)
    logging.info(result)
    nmap_exist = 'True'
except (subprocess.CalledProcessError, FileNotFoundError):
    install = webbrowser.open('https://nmap.org/download')
    logging.info(install)
    nmap_exist = 'False'


if nmap_exist == 'True':
    vulnerability_scanning(param)