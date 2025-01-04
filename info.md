Identify Bans – The proxy should be able to detect various types of blocking methods and fix the underlying problems 
                – i.e. captchas, redirects, blocks, ghosting, etc.

Retry Errors – Retry the request using a different proxy server if there are any connection problems, blocks, captchas, 
                etc with the current proxy.

Control Proxies – Few websites with authentication require to keep the session with the same IP or else authentication 
                    might be required again if there is any change in proxy server.

Adding Delays – Randomize delays and apply good throttling so the website cannot detect that you are scraping.

Geographical Location – Few websites may require IP’s from specific countries, so the proxy pool should contain 
                        the set of proxies from the given geolocation.

### How to use a proxy in requests module?
Import the requests module.
Create a pool of proxies and then rotate/iterate them.
Send a GET request using requests.get() by passing the proxy as a parameter to the URL.
Returns the proxy server address of the current session if there is no connection error.

# Import the required Modules
import requests

# Create a pool of proxies
proxies = {
    'http://114.121.248.251:8080',
    'http://222.85.190.32:8090',
    'http://47.107.128.69:888',
    'http://41.65.146.38:8080',
    'http://190.63.184.11:8080',
    'http://45.7.135.34:999',
    'http://141.94.104.25:8080',
    'http://222.74.202.229:8080',
    'http://141.94.106.43:8080',
    'http://191.101.39.96:80'
}

url = 'https://ipecho.net/plain'

# Iterate the proxies and check if it is working.
for proxy in proxies:
    try:
        # https://ipecho.net/plain returns the ip address
        # of the current session if a GET request is sent.
        page = requests.get(
          url, proxies={"http": proxy, "https": proxy})

        # Prints Proxy server IP address if proxy is alive.
        print("Status OK, Output:", page.text)

    except OSError as e:
        # Proxy returns Connection error
        print(e)