from pathlib import Path

async def process(file_path: Path):
    """
    Example preprocessing rule that adds a comment to the start of a G-code file.
    
    Args:
        file_path: Path to the uploaded file
    """
    if file_path.suffix.lower() in ['.gcode', '.g']:
        content = file_path.read_text()
        with open(file_path, 'w') as f:
            f.write("; Processed by Moonraker Preprocessing Proxy\n")
            f.write(content)
