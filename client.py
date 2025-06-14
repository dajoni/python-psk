import requests
import ssl
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# PSK configuration (must match server)
PSK_IDENTITY = "client1"
PSK_KEY = bytes.fromhex('c0ffee')

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
    """Create SSL context with TLS 1.2 and PSK"""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    
    # Enable PSK
    context.set_psk_client_callback(psk_callback)
    
    # Set cipher suites that support PSK
    context.set_ciphers('PSK')
    
    
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
    
    # Make request to the server
    try:
        response = session.get('https://127.0.0.1:5000/hello')
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main() 