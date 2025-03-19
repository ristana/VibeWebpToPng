import PyInstaller.__main__
import os
import sys
import site
import tkinterdnd2
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    print("Starting build process...")
    
    # Get the absolute path to the icon file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find tkdnd package location
    tkdnd_root = os.path.dirname(tkinterdnd2.__file__)
    tkdnd_path = os.path.join(tkdnd_root, 'tkdnd')
    tkdnd_path_alt = os.path.join(tkdnd_root, 'tk')
    
    # Use alternate path if main path doesn't exist
    if not os.path.exists(tkdnd_path) and os.path.exists(tkdnd_path_alt):
        tkdnd_path = tkdnd_path_alt
    
    # Find all DLL files
    dll_files = []
    for root, dirs, files in os.walk(tkdnd_root):
        for file in files:
            if file.endswith('.dll'):
                dll_files.append(os.path.join(root, file))
    
    # Create a temporary directory for DLLs
    temp_dll_dir = os.path.join(script_dir, 'temp_dlls')
    os.makedirs(temp_dll_dir, exist_ok=True)
    
    # Copy DLLs to temp directory
    for dll in dll_files:
        shutil.copy2(dll, temp_dll_dir)
    
    # PyInstaller arguments
    args = [
        'src/main.py',  # Your main script
        '--name=WebP-to-PNG',  # Name of the executable
        '--noconsole',  # Don't show console window
        '--onefile',  # Create a single executable file
        '--clean',  # Clean PyInstaller cache
        f'--add-data={tkdnd_path};tkdnd',  # Include tkdnd package
        f'--add-data={temp_dll_dir}/*;.',  # Include DLLs in root
        '--add-data=README.md;.',  # Include README
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--hidden-import=customtkinter',
        '--hidden-import=tkinterdnd2',
        '--collect-all=tkinterdnd2',
    ]
    
    # Add platform-specific options
    if sys.platform.startswith('win'):
        args.extend([
            '--windowed',  # Windows specific no-console flag
        ])
    
    print("Building with PyInstaller...")
    print(f"Including tkdnd from: {tkdnd_path}")
    print(f"Including DLLs from: {temp_dll_dir}")
    PyInstaller.__main__.run(args)
    
    # Clean up temp directory
    shutil.rmtree(temp_dll_dir, ignore_errors=True)
    
    print("Build complete! Check the 'dist' directory for your executable.")

if __name__ == "__main__":
    build_executable() 