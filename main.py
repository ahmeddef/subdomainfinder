import sublist3r
import requests

def get_subdomains(domain):
    subdomains = sublist3r.main(domain, 40, None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    return subdomains

def get_status_code(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.RequestException as e:
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_subdomains.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    try:
        subdomains = get_subdomains(domain)
        for subdomain in subdomains:
            url = f"http://{subdomain}"
            status_code = get_status_code(url)
            if status_code:
                print(f"{subdomain} - Status Code: {status_code}")
            else:
                print(f"{subdomain} - Status Code: Not reachable")
        print("STATUS_CODE: 0")  # Indicate success
    except Exception as e:
        print(f"Error: {e}")
        print("STATUS_CODE: 1")  # Indicate error
