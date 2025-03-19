# Current Sprint Tasks

## CORE-001: Essential WebP to PNG Converter
Status: In Progress
Priority: High
Dependencies: None

### Requirements
- Single window GUI with drag-drop zone
- WebP to PNG conversion
- Success/error messages
- Progress indication

### Acceptance Criteria
1. Window opens and accepts drag-drop
2. WebP files convert to PNG successfully
3. User gets clear feedback on success/failure
4. Output PNGs maintain quality
5. Application works as standalone executable

### Technical Notes
- Use CustomTkinter for GUI
- Use Pillow for conversion
- Handle large files with threading
- Package with PyInstaller

## Future Enhancements
Status: Planned
Priority: Low

### Batch Processing
- Multiple file selection
- Progress tracking
- Cancellation support

### Quality of Life
- Custom output directory
- Preview functionality
- Additional format support

## Development Checklist

### Phase 1: Core Functionality ✅
- [x] Project structure
- [x] Basic GUI window
- [x] File conversion logic
- [ ] Basic drag-drop
- [ ] Basic drag-drop multiple files

### Phase 2: Polish (In Progress)
- [ ] Progress feedback
- [ ] Error messages
- [ ] Threading for large files
- [ ] Executable packaging

### Phase 3: Testing
- [ ] Core functionality testing
- [ ] Large file handling
- [ ] Error cases
- [ ] Cross-platform checks 