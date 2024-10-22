"""Take an ip and scan their open ports using Shodan API."""

import logging
import argparse
import json
import shodan

# Generate a config for the file error
logging.basicConfig(
    filename="APIRequest_Errors.log",
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.ERROR,
)

# Generate a config for the file info
logging.basicConfig(
    filename="API_Actions.log",
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

# Create an argument for the sripts run
mode = """
Run the next command:
python ip_openports_scan.py -ip 'target ip'
"""
ips = argparse.ArgumentParser(
    description="IPs to make the scan of their ports",
    epilog=mode,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
ips.add_argument(
    "-ip",
    metavar="IP",
    dest="ip",
    type=str,
    help="IP to analyze their ports",
    required=True,
)

arguments = ips.parse_args()
ip = ips.ip

# The shodan api key to authenticate our search in the api
api_key = "qYsYnBh8c6vx820iWeJc9VwzFMcIUU5l"
logging.info("Key registrada : %s" % api_key)
try:
    api = shodan.Shodan(api_key)
except shodan.APIError as error:
    print(">> Ocurrió un error con la API: \n%s" % error)
    logging.error(f"Error: {error}")
else:
    logging.info("API conecction created successfully :D")

    # Save the response in a txt file to make reading easier
    with open("API_IPResponse.txt", "w") as file:
        try:
            response = api.host(ip)
            file.write(f"<< Open ports in IP : {ip} >>\n")
            for port in response["ports"]:
                file.write(f"> {port} <\n")
            file.write("Scan complete, Have a nice day :D")

        except shodan.APIError as error:
            print(">> Ocurrió un error con la API: \n%s" % error)
            logging.error(f"Error: {error}")

        except Exception as error:
            print(">> Ocurrió un error: \n%s" % error)
            logging.error(f"Error: {error}")

        else:
            response = api.host(ip)
            full_response_file_name = "Full_API_Response.txt"
            with open(full_response_file_name, "w") as file:
                data = json.dumps(response, indent=4)
                file.write(data)
            logging.info(
                'Data requested are saved in API_IPRespobse.txt'
                '\n And the full info requested are in %s'
                % full_response_file_name
            )
            print("Scan completed for the ip: %s" % ip)

        finally:
            print(
                "The full response and error.log files are created"
                " with the IP scan requested"
            )
            logging.info("Execution completed have a nice day :D")
