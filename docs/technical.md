# WebP to PNG Converter - Technical Documentation

## Core Functionality

1. **Single Window Interface**
   - Drag-and-drop zone for WebP files
   - Clear success/error messages
   - Progress indication for large files
   - Minimal, user-friendly design

2. **Image Conversion**
   - WebP to PNG conversion using Pillow
   - Maintains original image quality
   - Handles large files via threading
   - Saves in same directory as source

## Key Components

### GUI (app_window.py)
- CustomTkinter window
- Drag-drop functionality
- Status updates
- Error display

### Converter (converter.py)
- Image processing logic
- File validation
- Error handling
- Progress tracking

## Dependencies
- Python 3.8+
- CustomTkinter 5.2.2
- Pillow 10.1.0

## Implementation Guidelines

### Error Handling
1. Validate input files
2. Show clear error messages
3. Handle conversion failures
4. Prevent UI freezing

### Threading
1. Convert large files in background
2. Update progress in main thread
3. Keep UI responsive
4. Handle cancellation

### File Management
1. Validate WebP format
2. Check write permissions
3. Handle path issues
4. Preserve file quality

## Distribution
- Package with PyInstaller
- Include all dependencies
- Create single executable
- Test on target platforms 