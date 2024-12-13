import json
import os
from termcolor import colored
import sys

def process_arb_files(path):
    """
    Process a single ARB file and convert it to Verblaze format.
    """
    if not path.endswith('.arb'):
        print(colored("\nOnly .arb files are supported!", "red"))
        sys.exit(1)
        
    try:
        with open(path, 'r', encoding='utf-8') as file:
            arb_data = json.load(file)
    except json.JSONDecodeError:
        print(colored("\nInvalid ARB file format!", "red"))
        sys.exit(1)
    
    # Convert to Verblaze format
    file_name = os.path.basename(path).replace('.arb', '')
    file_title = file_name.replace('_', ' ').title()
    
    values = {}
    for key, value in arb_data.items():
        if not key.startswith('@'):  # Skip metadata entries
            values[key] = value
            
    formatted_data = [{
        "file_title": "Main Translation",
        "file_key": "main",
        "values": values
    }]
    
    return json.dumps(formatted_data) 