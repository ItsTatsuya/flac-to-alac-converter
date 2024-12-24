# FLAC to ALAC Converter

A simple GUI application to convert FLAC audio files to Apple Lossless Audio Codec (ALAC) format.

![Screenshot](https://i.imgur.com/T3bHg2v.png)

[![License](https://img.shields.io/github/license/ItsTatsuya/flac-to-alac-converter?style=for-the-badge)](LICENSE)

[![Issues](https://img.shields.io/github/issues/ItsTatsuya/flac-to-alac-converter?style=for-the-badge)](https://github.com/ItsTatsuya/flac-to-alac-converter/issues)

[![Download Latest Release](https://img.shields.io/github/v/release/YourUsername/flac-to-alac-converter?style=for-the-badge&label=Download)](https://github.com/ItsTatsuya/flac-to-alac-converter/releases/latest)

## Built With

- [Python](https://www.python.org/)
- [PyInstaller](https://www.pyinstaller.org/)
- [ffmpeg](https://ffmpeg.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
## Features

- Drag and drop interface for FLAC files
- Batch conversion support
- Progress tracking
- Custom output folder selection
- Modern UI with Sun Valley theme

## Installation
1. Download the latest release from the [releases page](https://github.com/ItsTatsuya/flac-to-alac-converter/releases/latest)
2. Run the **FlaskToAlacConverter.exe** file
3. Enjoy!

## Usage

1. Add FLAC files by:
   - Dragging and dropping files/folders onto the application window
   - Using the "Add Files" button to select individual files
   - Using the "Add Folder" button to select entire folders
2. Select an output folder using the "Browse" button
3. Click "Convert Files" to start the conversion process

## Requirements

- Windows 10/11
- No additional software required - all dependencies are bundled with the executable

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests if applicable
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

### Development Setup

```sh
# Clone the repository
git clone https://github.com/ItsTatsuya/flac-to-alac-converter.git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/gui.py
