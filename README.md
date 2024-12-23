# Moonraker Preprocessing Proxy

A proxy server that sits between your slicer and Moonraker, allowing custom preprocessing of uploaded files while passing through all other commands directly to Moonraker.

## Features

- Intercepts file upload commands for preprocessing
- Passes through all other commands directly to Moonraker
- Configurable preprocessing rules/scripts
- Simple and lightweight

## Requirements

- pyenv (for Python version management)
- Python 3.11+ (will be installed via pyenv)
- Dependencies will be installed in a virtual environment

## Installation

1. Install pyenv and Python build dependencies:
```bash
# Install pyenv dependencies
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl

# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc
```

2. Clone this repository:
```bash
git clone https://github.com/yourusername/MoonrakerPreProcessingProxy.git
cd MoonrakerPreProcessingProxy
```

3. Set up Python environment:
```bash
# Install Python 3.11.6
pyenv install 3.11.6

# Set local Python version
pyenv local 3.11.6

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

4. Configure your preprocessing rules in `config.yaml`

5. Set up systemd service for auto-start:
```bash
# Copy the service file to systemd directory
sudo cp moonraker-proxy.service /etc/systemd/system/
sudo systemctl daemon-reload
```

6. Enable and start the service:
```bash
sudo systemctl enable moonraker-proxy
sudo systemctl start moonraker-proxy
```

7. Check service status:
```bash
sudo systemctl status moonraker-proxy
```

## Development

For development, you can run the proxy manually:
```bash
source .venv/bin/activate
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
