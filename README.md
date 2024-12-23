# Moonraker Preprocessing Proxy

A proxy server that sits between your slicer and Moonraker, allowing custom preprocessing of uploaded files while passing through all other commands directly to Moonraker.

## Features

- Intercepts file upload commands for preprocessing
- Passes through all other commands directly to Moonraker
- Configurable preprocessing rules/scripts
- Simple and lightweight

## Requirements

- Python 3.7+
- FastAPI
- httpx
- python-multipart
- uvicorn

## Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/MoonrakerPreProcessingProxy.git
cd MoonrakerPreProcessingProxy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your preprocessing rules in `config.yaml`

4. Set up systemd service for auto-start:
```bash
# Copy the service file to systemd directory
sudo cp moonraker-proxy.service /etc/systemd/system/
sudo systemctl daemon-reload
```

5. Enable and start the service:
```bash
sudo systemctl enable moonraker-proxy
sudo systemctl start moonraker-proxy
```

6. Check service status:
```bash
sudo systemctl status moonraker-proxy
```

7. Run the proxy:
```bash
python main.py
```

## Configuration

The proxy listens on port 7125 by default and forwards requests to Moonraker (default: http://localhost:7125).

### Preprocessing Rules

Define your preprocessing rules in `config.yaml`. Each rule is a script that will be executed in order when a file is uploaded.

## Usage

1. Configure your slicer to use the proxy address instead of direct Moonraker address
2. Upload files as normal - they will be preprocessed before being sent to Moonraker
3. All other commands (non-file-upload) will be passed through directly

## License

MIT
