"""Take a url and scan its vulnerabilities with ZAP, return a html report."""

import os
import time
import psutil
import logging
import argparse
import requests
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup
import pyautogui
from zapv2 import ZAPv2
from menu import main_menu

mainproxy = "http://localhost:8080"  # zap proxy

mode = """
Run the following command:
python scanweb.py -url 'target_url' -zapikey 'apikey_from_zap'

Ideal scenario
- You install ZAP from https://www.zaproxy.org/download/\
 and create a new ZAP session before run this script.

Notes
- this script requires ZAP installed on\
your computer (https://www.zaproxy.org/download/)
- you need your personal apikey, you get it in the ZAP software\
once installed, where? Tools>Options>API>API Key
- if a popup window opens when you start ZAP with the prompt\
to create a session, remove the window or click “OK”.
- this script will in turn overwrite a ZAP session called “webpentest_session”.
- active scanning usually takes longer than spider scanning
"""
parser = argparse.ArgumentParser(
    description="This script shows vulnerabilities from a web page.",
    epilog=mode,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "-url", metavar="URL", dest="url", help="url to scan", required="True"
)
parser.add_argument(
    "-zapikey",
    metavar="ZAP_APIKEY",
    dest="zapikey",
    help="this apikey is offered by zap when you install it",
    required="True",
)

parameters = parser.parse_args()
target_url = parameters.url
zapikey = parameters.zapikey

zap_request = ZAPv2(
    apikey=zapikey, proxies={"http": mainproxy, "https": mainproxy}
)  # Connection with zaproxy
logging.basicConfig(
    filename="zapLog.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)  # Logs settings

# initializing some variables
zap_is_installed = zap_is_running = zap_is_connected = False
found_zap_process = java_process = False
process = None

print("==== Welcome to this web pentest with ZAP ====")
print("Logging everything, visit -zapLog.log- when ready.")

pc_dirs = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
for pc_dir in pc_dirs:
    # search zap in my system
    for root, dirs, files in os.walk(pc_dir):
        if "ZAP.exe" in files:
            zap_exe_path = str(os.path.join(root, "ZAP.exe"))
            logging.info(f"ZAP is installed: {zap_exe_path}")
            zap_is_installed = True


def process_iter(java_process, found_zap_process, zap_is_running, process):
    """Return information about java and zap process."""
    for process in psutil.process_iter(["name", "cmdline"]):
        if process.info["name"] == "java.exe"\
                or process.info["name"] == "javaw.exe":
            java_process = True
            if any("zap" or "ZAP" in arg.lower() for arg in process.info["cmdline"]):
                found_zap_process = True
                logging.info("ZAP is running...")
                zap_is_running = True
                break
    return java_process, found_zap_process, zap_is_running, process


if zap_is_installed:
    logging.info(f"Starting script for web pentesting to {target_url}")

    # call process_iter function
    java_process, found_zap_process, zap_is_running, process = process_iter(
        java_process, found_zap_process, zap_is_running, process
    )

    if not found_zap_process:
        logging.info("Running ZAP...")
        time.sleep(3)
        pyautogui.hotkey("win", "r")  # uses a keyboard combo to start zap
        time.sleep(3)
        pyautogui.typewrite(zap_exe_path)
        time.sleep(3)
        pyautogui.press("enter")
        for i in range(0, 120, 30):
            # review connection every 30 sec from 2 min
            logging.info(f"Try #{(i//30)+1}")
            try:
                zap_connection = requests.get(mainproxy)
                if zap_connection.status_code == 200:  # if connection is OK
                    zap_request.core.new_session(
                        name="webpentest_session", overwrite=True
                    )  # start a new zap session
                    zap_is_connected = True
                    break
            except requests.ConnectionError:
                logging.warning("Trying to connect with ZAP again...")
            time.sleep(30)
    if zap_is_connected:
        logging.info("ZAP connection was established.")
    else:
        logging.warning("Unable to connect with ZAP after 2 min...")

else:
    logging.error(
        """ZAP was not located in the system.
    Redirecting to the download page..."""
    )
    print("Please, install ZAP and run this script again.")
    webbrowser.open(
        "https://www.zaproxy.org/download/"
    )  # open this page to install zap
    main_menu()  # end script because zap was not installed

# call function to CONFIRM that zap is running and save zap process
java_process, found_zap_process, zap_is_running, process = process_iter(
    java_process, found_zap_process, zap_is_running, process
)
time.sleep(10)  # give time to make the process iter from psutils
if zap_is_running:
    try:
        logging.info(f"Starting web pentesting to {target_url}")
        zap_request.core.new_session(name="webpentest_session", overwrite=True)

        spider_progress = zap_request.spider.scan(target_url)
        while int(zap_request.spider.status(target_url)) < 100:
            logging.info(
                f"Spider scan progress ---- {zap_request.spider.status(spider_progress)}%"
            )
            time.sleep(5)
        logging.info(f"Completed spider scan to {target_url}")

        zap_request.urlopen(target_url)
        time.sleep(3)

        active_progress = zap_request.ascan.scan(target_url)
        while int(zap_request.ascan.status(target_url)) < 100:
            logging.info(
                f"Active scan progress ---- {zap_request.ascan.status(active_progress)}%"
            )
            time.sleep(5)
        logging.info(f"Completed active scan to {target_url}")

        vulnerabilities = zap_request.core.alerts(baseurl=target_url)
        logging.info(
            f"{len(vulnerabilities)} vulnerabilities were found in {target_url}"
        )

    except Exception as e:
        logging.error(f"Error when scanning {target_url} >> {e}")

    html_report = zap_request.core.htmlreport()  # Get html report from ZAP api
    epoch_date = int(datetime.now().timestamp())
    report_name = f"WebPentest{epoch_date}.html"

    with open(report_name, "w", encoding="utf-8") as report:
        report.write(html_report)  # save html content

    # to personalize report html title with just url domain
    domain = (
        target_url.replace("http://", "")
        .replace("https://", "")
        .replace("www.", "")
        .split("/")[0]
    )
    soup = BeautifulSoup(html_report, "html.parser")
    soup.title.string = f"{domain} SCAN REPORT"  # modify title

    with open(report_name, "w", encoding="utf-8") as file:
        file.write(str(soup))  # save this change

    # Notice that the report was created
    logging.info(f"Report {report_name} created.")
    print(f"ZAP vulnerabilities report {report_name} available.")

    try:
        # close ZAP
        process.kill()
        logging.info("ZAP's task is finished here. Thank you.")
    except Exception:
        print("Cannot found ZAP to close it. Please try to close it manually.")
        logging.warning("Close ZAP, please.")
    finally:
        # always announces the end of the script
        print("END.")
        logging.info("END.")
else:
    # if zap could never be open...
    print("WARNING!! Please check our ZAP log file.")
    logging.error(
        """ZAP could never be started.
    This script will not work if ZAP is not running on your computer."""
    )
main_menu()
