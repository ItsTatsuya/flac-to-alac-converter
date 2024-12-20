import os
from pathlib import Path

def validate_flac_file(file_path):
    """Check if the provided file path is a valid FLAC file."""
    return os.path.isfile(file_path) and file_path.endswith('.flac')

def create_output_directory(output_dir):
    """Create the output directory if it does not exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def get_output_file_path(input_file_path, output_dir):
    """Generate the output file path for the converted ALAC file."""
    base_name = os.path.basename(input_file_path)
    output_file_name = os.path.splitext(base_name)[0] + '.m4a'
    return os.path.join(output_dir, output_file_name)