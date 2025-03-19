# WebP to PNG Converter

A modern, efficient desktop application for converting WebP images to PNG format. Features a sleek dark theme interface and support for batch conversions.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)

## Features

- 🎨 Modern dark theme interface
- 📁 Drag and drop multiple WebP files
- 🔄 Batch conversion to PNG format
- 📊 Real-time progress tracking
- ✨ Clear status messages and notifications
- 🔒 No quality loss in conversion
- 🚀 Background processing for large files
- 💻 Standalone executable - no installation needed

## Quick Start

1. Download the latest release (`WebP-to-PNG.exe`)
2. Run the executable
3. Drag and drop one or more WebP files onto the window
4. Watch the progress as files are converted
5. Find the converted PNG files in the same directory as the original files

## System Requirements

- Windows 10 or later
- No additional software required (standalone executable)
- Minimum 4GB RAM recommended for large batch operations

## Usage Tips

- **Multiple Files**: Drag multiple files at once for batch conversion
- **Progress Tracking**: Watch real-time progress for each file
- **Status Updates**: Clear notifications for successful conversions and any errors
- **File Location**: Converted PNGs are saved in the same directory as source files
- **Large Files**: Application remains responsive during large file conversions

## Technical Details

Built with:
- Python 3.9+
- CustomTkinter for modern UI
- Pillow for image processing
- Threading for background operations
- TkinterDnD2 for drag-and-drop support

## Development

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running from Source
```bash
python src/main.py
```

### Building Executable
```bash
python build.py
```

## Version History

### v1.0.0 (2024)
- Initial release
- Dark theme modern interface
- Multiple file drag-and-drop
- Batch conversion support
- Progress tracking
- Background processing
- Standalone executable

## License

MIT License - Feel free to use and modify as needed.

## Acknowledgments

- CustomTkinter for the modern UI components
- Pillow for reliable image processing
- TkinterDnD2 for drag-and-drop functionality

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