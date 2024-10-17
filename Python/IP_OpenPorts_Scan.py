import logging
import argparse
import json
import shodan

# Generate a config for the file error
logging.basicConfig(filename='APIRequest_Errors.log',
                    format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %H:%M:%S",
                    level=logging.ERROR)

# Create an argument for the sripts run
ips = argparse.ArgumentParser(description="IPs to make the scan of their ports")
ips.add_argument("-ip", dest='IP',type=str, help="IP to analyze ", required=True)

# The shodan api key to authenticate our search in the api
api_key = 'qYsYnBh8c6vx820iWeJc9VwzFMcIUU5l'
try:
    api = shodan.Shodan(api_key)
except shodan.APIError as error:
    print('>> Ocurrió un error con la API: \n%s' % error)
    logging.error(f"Error: {error}")

# Save the response in a txt file to make reading easier
with open('API_IPResponse.txt', 'w') as file:
    try:
        ip = ips.parse_args()
        response = api.host(ip.IP)
        file.write(f"<< Open ports in IP : {ip.IP} >>\n")
        for port in response['ports']:
            file.write(f"> {port} <\n")
        file.write("Scan complete, Have a nice day :D")

    except shodan.APIError as error:
        print('>> Ocurrió un error con la API: \n%s' % error)
        logging.error(f"Error: {error}")

    except Exception as error:
        print('>> Ocurrió un error: \n%s' % error)
        logging.error(f"Error: {error}")

    else:
        response = api.host(ip.IP)
        full_response_file_name = 'Full_API_Response.txt'
        with open(full_response_file_name, 'w') as file:
            data = json.dumps(response, indent=4)
            file.write(data)
    
    finally:
        print("The full response and error.log files are created"\
              " with the IP scan requested")
