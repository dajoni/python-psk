# TLS 1.2 PSK REST Server

This is a simple REST server that uses TLS 1.2 with Pre-Shared Key (PSK) authentication. The server provides a basic "hello world" endpoint.

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
- The server uses TLS 1.2 with PSK authentication, which provides forward secrecy and strong security guarantees.
- Certificate verification is disabled in the client since we're using PSK authentication instead of certificates.

## API Endpoints

- `GET /hello`: Returns a simple "Hello, World!" message in JSON format. 

# Distribution
Install pex and do
```bash
pex $(pip freeze) --scie eager --scie-only --exe server.py -o my_test.pex
```