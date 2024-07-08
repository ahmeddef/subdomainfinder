import sublist3r
import requests
import argparse
import sys

def get_subdomains(domain):
    subdomains = sublist3r.main(domain, 40, None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    return subdomains

def get_status_code(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.RequestException:
        return None

def save_output_to_file(output, file_path):
    with open(file_path, 'w') as f:
        f.write(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get subdomains and their status codes.")
    parser.add_argument("domain", help="The domain to find subdomains for.")
    parser.add_argument("-o", "--output", help="The file to save the output to.")
    parser.add_argument("-f", "--filter", type=int, nargs='*', help="Filter by status codes.")
    args = parser.parse_args()

    domain = args.domain
    output_file = args.output
    filter_codes = args.filter

    try:
        subdomains = get_subdomains(domain)
        output = ""
        for subdomain in subdomains:
            url = f"http://{subdomain}"
            status_code = get_status_code(url)
            if status_code:
                line = f"{subdomain} - Status Code: {status_code}\n"
            else:
                line = f"{subdomain} - Status Code: Not reachable\n"
            if not filter_codes or (status_code in filter_codes if status_code else False):
                output += line
                print(line, end="")

        final_status = "STATUS_CODE: 0\n"  # Indicate success
        output += final_status
        print(final_status, end="")

        if output_file:
            save_output_to_file(output, output_file)
    except Exception as e:
        error_message = f"Error: {e}\nSTATUS_CODE: 1\n"
        print(error_message, end="")
        if output_file:
            save_output_to_file(error_message, output_file)
        sys.exit(1)
