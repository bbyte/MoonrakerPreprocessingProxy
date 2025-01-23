from pathlib import Path
import re

async def process(file_path: Path):
    """
    Preprocessing rule for OrcaSlicer multi-extruder files that:
    1. Comments out M600 commands before either ";TYPE:Skirt" or BEFORE_LAYER_CHANGE marker
    2. Comments out standalone T[n] commands throughout the file
    3. Removes T[n] part from M104 and M109 commands
    
    Args:
        file_path: Path to the uploaded file
    """
    print(f"[INFO] OrcaSlicer multi-extruder rule processing file: {file_path}")
    
    if file_path.suffix.lower() not in ['.gcode', '.g']:
        print(f"[INFO] Skipping non-gcode file: {file_path}")
        return
        
    print(f"[INFO] Modifying G-code file: {file_path}")
    
    # Read the file content
    with open(file_path, 'rb') as f:
        content = f.read()
        
    # Convert to text for processing, keeping original line endings
    text_content = content.decode('utf-8')
    lines = text_content.splitlines(keepends=True)
    
    # Process the file
    found_print_start = False  # Will be set to True when either marker is found
    modified_lines = []
    
    # Add header comments
    modified_lines.append("; File modified by Moonraker Preprocessing Proxy\n")
    modified_lines.append("; Rule: OrcaSlicer Multi-Extruder Cheating\n")
    modified_lines.append("\n")
    
    for line in lines:
        # Check for either marker - whichever comes first
        if not found_print_start and (";TYPE:Skirt" in line or "BEFORE_LAYER_CHANGE" in line):
            found_print_start = True
            modified_lines.append(line)
            continue
            
        # Before either marker is found, comment out M600 commands
        if not found_print_start and re.match(r'^\s*M600\s*$', line.strip()):
            modified_lines.append(f";{line.rstrip()} ; commented out by OrcaSlicer Multi-Extruder Cheating\n")
            continue
                
        # Process M104 and M109 commands - remove T[n] part if present
        if line.strip().startswith('M104'):
            if 'preheat' in line.lower():
                # Comment out the entire line if it contains preheat
                modified_lines.append(f";{line.rstrip()} ; commented out by OrcaSlicer Multi-Extruder Cheating\n")
            else:
                # Remove T[n] part but keep the rest of the command
                modified_line = re.sub(r'\bT\d+\s*', '', line)
                if modified_line != line:
                    modified_lines.append(f"{modified_line.rstrip()} ; T[n] removed by OrcaSlicer Multi-Extruder Cheating\n")
                else:
                    modified_lines.append(line)
        elif line.strip().startswith('M109'):
            # Remove T[n] part but keep the rest of the command
            modified_line = re.sub(r'\bT\d+\s*', '', line)
            if modified_line != line:
                modified_lines.append(f"{modified_line.rstrip()} ; T[n] removed by OrcaSlicer Multi-Extruder Cheating\n")
            else:
                modified_lines.append(line)
        # Comment out standalone T[n] commands
        elif re.match(r'^\s*T\d+\s*$', line.strip()):
            modified_lines.append(f";{line.rstrip()} ; commented out by OrcaSlicer Multi-Extruder Cheating\n")
        else:
            modified_lines.append(line)
    
    # Write modified content back to file
    with open(file_path, 'w', newline='') as f:
        f.writelines(modified_lines)
            
    print(f"[INFO] Successfully modified file: {file_path}")
