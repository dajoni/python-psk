import requests
import ssl
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# PSK configuration (must match server)
PSK_IDENTITY = "client1"
PSK_KEY = bytes.fromhex('b0ffee')

class SSLContextAdapter(requests.adapters.HTTPAdapter):
    """Transport adapter that uses a custom SSL context."""
    def __init__(self, ssl_context, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        pool_kwargs['ssl_context'] = self.ssl_context
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            **pool_kwargs
        )

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        proxy_kwargs['ssl_context'] = self.ssl_context
        return super().proxy_manager_for(proxy, **proxy_kwargs)


def psk_callback(identity):
    """Callback function for PSK authentication"""
    return PSK_IDENTITY, PSK_KEY
    

def create_ssl_context():
    """Create SSL context with TLS 1.3 and PSK"""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    
    # Enable PSK
    context.set_psk_client_callback(psk_callback)
    
    # TLS 1.3 handles PSK ciphers automatically, no need to set specific ciphers
    
    
    return context

def main():
    # Create SSL context
    ssl_context = create_ssl_context()
    
    
    # Use the custom SSLContextAdapter
    adapter = SSLContextAdapter(ssl_context)

    # Create a custom session with the SSL context
    session = requests.Session()
    session.verify = False  # Disable certificate verification since we're using PSK
    
    # Configure the session to use our SSL context
    session.mount('https://', adapter)
    
    # Server configuration
    base_url = 'https://127.0.0.1:5000'
    
    # Test both server endpoints
    endpoints = ['/', '/hello']
    
    connection_failed = False
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"Testing endpoint: {url}")
            response = session.get(url)
            print(f"Response: {response.json()}")
            print("-" * 50)
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error for {url}: {e}")
            print("-" * 50)
            connection_failed = True
        except requests.exceptions.SSLError as e:
            print(f"SSL error for {url}: {e}")
            print("-" * 50)
            connection_failed = True
        except requests.exceptions.Timeout as e:
            print(f"Timeout error for {url}: {e}")
            print("-" * 50)
            connection_failed = True
        except requests.exceptions.RequestException as e:
            print(f"Request error for {url}: {e}")
            print("-" * 50)
            connection_failed = True
        except Exception as e:
            print(f"Unexpected error for {url}: {e}")
            print("-" * 50)
            connection_failed = True
    
    # Return appropriate exit code
    if connection_failed:
        print("Connection failed - exiting with error code 1")
        return 1
    else:
        print("All connections successful")
        return 0

if __name__ == '__main__':
    sys.exit(main()) 
