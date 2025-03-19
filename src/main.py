import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.app_window import AppWindow

def main():
    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    main() 