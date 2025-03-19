import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import sys
from typing import List
from tkinterdnd2 import DND_FILES, TkinterDnD
from src.converter import ImageConverter, ConversionQueue, ConversionResult

def get_tkdnd_path():
    """Get the path to tkdnd package, handling both development and bundled cases"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS  # Root of all bundled files
        tkdnd_path = os.path.join(base_path, 'tkdnd')
        
        # Print debug info
        print(f"Bundle base path: {base_path}")
        print(f"Looking for tkdnd in: {tkdnd_path}")
        if os.path.exists(tkdnd_path):
            print(f"tkdnd directory contents: {os.listdir(tkdnd_path)}")
        else:
            print("tkdnd directory not found")
            
        # In bundled mode, DLLs are in the root directory
        return base_path
    else:
        # Running in development
        import tkinterdnd2
        base_path = os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tkdnd')
        alt_path = os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tk')
        
        if os.path.exists(base_path):
            return base_path
        elif os.path.exists(alt_path):
            return alt_path
        else:
            print(f"Development tkdnd paths not found: {base_path} or {alt_path}")
            return None

class AppWindow(TkinterDnD.Tk):
    def __init__(self):
        # Initialize Tkinter with tkdnd path
        tkdnd_path = get_tkdnd_path()
        if tkdnd_path:
            os.environ['TKDND_LIBRARY'] = tkdnd_path
            # Also add to system path for DLL loading
            if tkdnd_path not in os.environ['PATH']:
                os.environ['PATH'] = tkdnd_path + os.pathsep + os.environ['PATH']
        
        # Initialize Tk
        super().__init__()
        
        # Configure theme first
        ctk.set_appearance_mode("dark")  # Force dark mode
        ctk.set_default_color_theme("blue")
        
        # Configure window
        self.title("WebP to PNG Converter")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Configure window background color for title bar and borders
        self.configure(bg='#2b2b2b')
        
        # Create main frame with dark theme
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=("#2b2b2b", "#2b2b2b"),
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Create content frame for padding
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create drop zone with darker border
        self.drop_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent",
            border_width=2,
            border_color=("#404040", "#404040")
        )
        self.drop_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="Drag and drop WebP files here\nSupports multiple files",
            font=("Helvetica", 14),
            text_color=("gray90", "gray90")
        )
        self.drop_label.pack(expand=True)
        
        # Create status frame
        self.status_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.status_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Create progress bar with theme-appropriate colors
        self.progress_bar = ctk.CTkProgressBar(
            self.status_frame,
            fg_color=("#333333", "#333333"),
            progress_color=("#1f538d", "#1f538d")
        )
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        # Create notification label
        self.notification_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=("Helvetica", 12),
            text_color=("gray70", "gray70")
        )
        self.notification_label.pack(pady=(0, 5))
        
        # Create status label
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=("Helvetica", 12),
            text_color=("gray80", "gray80")
        )
        self.status_label.pack(pady=(0, 5))
        
        # Initialize conversion queue
        self.conversion_queue = ConversionQueue(
            on_file_complete=self._on_file_complete,
            on_batch_progress=self._on_batch_progress
        )
        
        # Configure drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self._handle_drop)
        
        # Bind hover events
        self.drop_frame.bind('<Enter>', self._handle_drag_enter)
        self.drop_frame.bind('<Leave>', self._handle_drag_leave)
        
    def _handle_drop(self, event) -> None:
        """Handle file drop event"""
        # Get the dropped files
        files = event.data.split()
        if files:
            # Reset progress bar and notifications
            self.progress_bar.set(0)
            self.notification_label.configure(text="")
            self.status_label.configure(text="Starting conversion...")
            
            # Add files to conversion queue
            self.conversion_queue.add_files(
                [f.strip('{}') for f in files]
            )
    
    def _on_file_complete(self, result: ConversionResult) -> None:
        """Handle completion of single file conversion"""
        if result.success:
            self.status_label.configure(
                text=f"Converted: {os.path.basename(result.output_path)}"
            )
            self.notification_label.configure(
                text=f"Success: {os.path.basename(result.input_path)} → PNG",
                text_color=("#00cf00", "#00cf00")  # Brighter green for dark theme
            )
        else:
            self.status_label.configure(
                text=f"Error: {os.path.basename(result.input_path)}"
            )
            self.notification_label.configure(
                text=f"Error: {os.path.basename(result.input_path)} - {result.error_message}",
                text_color=("#ff4444", "#ff4444")  # Brighter red for dark theme
            )
    
    def _on_batch_progress(self, completed: int, total: int) -> None:
        """Update progress bar and status for batch conversion"""
        progress = completed / total if total > 0 else 0
        self.progress_bar.set(progress)
        
        if completed == total:
            # Only show completion message if we have successful conversions
            successful_count = sum(1 for w in self.conversion_queue.completed_results if w.success)
            if successful_count > 0:
                self.status_label.configure(text="Ready")
                self.notification_label.configure(
                    text=f"Completed {successful_count} of {total} files successfully",
                    text_color=("#00cf00", "#00cf00")  # Brighter green for dark theme
                )
            else:
                self.status_label.configure(text="Ready")
                self.notification_label.configure(
                    text="No files were converted successfully",
                    text_color=("#ff4444", "#ff4444")  # Brighter red for dark theme
                )
    
    def _handle_drag_enter(self, event) -> None:
        """Handle drag enter event"""
        self.drop_frame.configure(border_color=("#1f538d", "#1f538d"))  # Darker blue
        self.drop_label.configure(text="Release to convert!")
        
    def _handle_drag_leave(self, event) -> None:
        """Handle drag leave event"""
        self.drop_frame.configure(border_color=("#404040", "#404040"))  # Back to default
        self.drop_label.configure(
            text="Drag and drop WebP files here\nSupports multiple files"
        ) 