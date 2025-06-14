from flask import Flask, jsonify
import ssl
import socket
import os

app = Flask(__name__)

# PSK configuration
PSK_IDENTITY = "client1"
PSK_KEY = bytes.fromhex('c0ffee')  # In production, use a secure key

def psk_callback(identity):
    """Callback function for PSK authentication"""
    print(f"PSK callback called with identity: {identity}")
    if identity == PSK_IDENTITY:
        return PSK_KEY
    return None

@app.route('/')
def index():
    print("Received request at root endpoint")
    return jsonify({"message": "Welcome to the PSK-enabled Flask server!"}) 

@app.route('/hello', methods=['GET'])
def hello_world():
    print("Received request at /hello endpoint")
    return jsonify({"message": "Hello, World!"})

def create_ssl_context():
    """Create SSL context with TLS 1.2 and PSK"""
    print("Creating SSL context with PSK support...")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    
    # Enable PSK
    context.set_psk_server_callback(psk_callback)
    
    # Set cipher suites that support PSK
    context.set_ciphers('PSK')
    
    return context

if __name__ == '__main__':
    # Create SSL context
    ssl_context = create_ssl_context()
        
    # print("Server running on https://localhost:5000") 
    
    # Run Flask app with SSL context
    app.run(ssl_context=ssl_context, debug=True) 
    # app.run() 