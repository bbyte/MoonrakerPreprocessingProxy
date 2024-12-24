# Moonraker Preprocessing Proxy

A proxy server that sits between your slicer and Moonraker, allowing custom preprocessing of uploaded files while passing through all other commands directly to Moonraker.

## Features

- Intercepts file upload commands for preprocessing
- Passes through all other commands directly to Moonraker
- Configurable preprocessing rules/scripts
- Simple and lightweight

## Requirements

- Python 3.7+
- Dependencies will be installed in a virtual environment

## Installation

1. Install Python and venv if not already installed:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv
```

2. Clone this repository:
```bash
git clone https://github.com/bbyte/MoonrakerPreprocessingProxy.git
cd MoonrakerPreProcessingProxy
```

3. Set up Python virtual environment:
```bash
# Create and activate virtual environment
python3 -m venv .venv
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

## Real-World Use Case: Multi-Color Single-Layer Printing

### The Challenge
This project was born from a specific need with the Bambu Lab V400 printer. While the V400 is a capable printer, it doesn't have a Multi-Material Unit (MMU). However, there was still a desire to print single layers with multiple colors, which typically requires manual filament changes.

### The Workaround
The solution involved "tricking" OrcaSlicer by configuring it to believe the printer has multiple extruders. This allows assigning different objects, modifiers, or parts of the print to specific "virtual" extruders. However, this approach came with its own challenges.

### The Problem
OrcaSlicer, being quite sophisticated, tries to manage these multiple extruders intelligently. It automatically adds:
- Preheating commands for each extruder
- Tool change commands (T0, T1, T2, etc.)
- Multiple M600 (filament change) commands
- Temperature controls with extruder specifications

Many of these automated additions are unnecessary or problematic for our single-extruder setup with manual filament changes.

### The Solution
This proxy server was created to intercept and modify the G-code files before they reach Moonraker. It implements specific rules to:
1. Remove unnecessary M600 and tool change commands before the print actually starts (before the skirt)
2. Strip out all standalone tool change commands (T0, T1, etc.)
3. Clean up temperature commands by removing extruder specifications
4. Comment out specific preheating commands

This "man-in-the-middle" approach allows for:
- Clean G-code that works with a single extruder
- Proper manual filament changes where needed
- Easy addition of new preprocessing rules as needed
- No modifications to either OrcaSlicer or Moonraker

The proxy's modular design means new rules can be added easily as new preprocessing needs are discovered, making it a flexible solution for various G-code manipulation requirements.

## Usage

1. Configure your slicer to use the proxy address instead of direct Moonraker address
2. Upload files as normal - they will be preprocessed before being sent to Moonraker
3. All other commands (non-file-upload) will be passed through directly

## License

MIT
