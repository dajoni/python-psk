# TLS 1.3 PSK REST Server

This is a simple REST server that uses TLS 1.3 with Pre-Shared Key (PSK) authentication. The server provides a basic "hello world" endpoint.

## Requirements

- Python 3.13+
- Flask
- pex

Install the requirements using:
```bash
pip install -r requirements.txt
```

## Running the Server

To start the server, run:
```bash
python server.py
```

The server will start on `https://127.0.0.1:5000`.

## Testing with the Client

To test the server using the provided client, run:
```bash
python client.py
```

## Security Notes

- The PSK identity and key are hardcoded for demonstration purposes. In a production environment, these should be securely stored and managed.
- The server uses TLS 1.3 with PSK authentication, which provides forward secrecy and strong security guarantees.
- Certificate verification is disabled in the client since we're using PSK authentication instead of certificates.

## API Endpoints

- `GET /hello`: Returns a simple "Hello, World!" message in JSON format. 

## Verifying PSK Authentication

To verify that the server is using PSK authentication and TLS 1.3:

### 1. OpenSSL s_client Test
```bash
# Test with correct PSK credentials (should succeed)
openssl s_client -connect 127.0.0.1:5000 -psk c0ffee -psk_identity client1 -tls1_3

# Test without PSK (should fail)
openssl s_client -connect 127.0.0.1:5000 -tls1_3
```

Look for:
- **"no peer certificate available"** - Confirms PSK instead of certificate authentication
- **"Protocol: TLSv1.3"** - Confirms TLS 1.3 negotiation
- **Cipher suite like "TLS_CHACHA20_POLY1305_SHA256"** - Modern TLS 1.3 cipher

### 2. Traffic Analysis
Capture and analyze network traffic:
```bash
# Capture traffic (requires sudo on most systems)
tcpdump -i lo0 -w psk_capture.pcap port 5000

# Run client to generate traffic
python client.py

# Analyze captured data
strings psk_capture.pcap | grep client1
strings psk_capture.pcap | grep -i hello
```

The PSK identity `client1` should be visible in the handshake, but application data (like "Hello, World!") should be encrypted and not visible.

# Distribution

```bash
pex $(pip freeze) --scie eager --scie-only --exe server.py -o my_test.pex
```
