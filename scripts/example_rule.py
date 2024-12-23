from pathlib import Path

async def process(file_path: Path):
    """
    Example preprocessing rule that adds a comment to the start of a G-code file.
    
    Args:
        file_path: Path to the uploaded file
    """
    print(f"[INFO] Example rule processing file: {file_path}")
    
    if file_path.suffix.lower() in ['.gcode', '.g']:
        print(f"[INFO] Modifying G-code file: {file_path}")
        content = file_path.read_text()
        with open(file_path, 'w') as f:
            f.write("; Processed by Moonraker Preprocessing Proxy\n")
            f.write("; Example rule was here\n")
            f.write(content)
        print(f"[INFO] Successfully modified file: {file_path}")
    else:
        print(f"[INFO] Skipping non-gcode file: {file_path}")
