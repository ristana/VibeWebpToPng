# WebP to PNG Converter

A modern desktop application that converts WebP images to PNG format with a simple drag-and-drop interface.

## Features

- Modern GUI with drag-and-drop support
- WebP to PNG conversion
- Success notifications
- Easy-to-use interface

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python src/main.py
   ```
2. Drag and drop WebP images onto the application window
3. Converted PNG files will be saved in the same directory as the original files

## Project Structure

```
webp_to_png/
├── src/
│   ├── main.py              # Main application entry point
│   ├── converter.py         # Image conversion logic
│   └── gui/
│       └── app_window.py    # GUI implementation
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Building Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed src/main.py
   ```

The executable will be created in the `dist` directory. 