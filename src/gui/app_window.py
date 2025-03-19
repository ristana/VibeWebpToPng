import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
from typing import Callable
from src.converter import ImageConverter

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("WebP to PNG Converter")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Configure theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create drop zone
        self.drop_label = ctk.CTkLabel(
            self.main_frame,
            text="Drag and drop WebP files here",
            font=("Helvetica", 14)
        )
        self.drop_label.pack(pady=20)
        
        # Create status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready",
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=10)
        
        # Configure drag and drop
        self.drop_target_register(tk.DND_FILES)
        self.dnd_bind('<<Drop>>', self._handle_drop)
        
        # Bind hover events
        self.drop_label.bind('<Enter>', self._handle_drag_enter)
        self.drop_label.bind('<Leave>', self._handle_drag_leave)
        
    def _handle_drop(self, event):
        """Handle file drop event"""
        # Get the dropped files
        file_path = event.data
        if file_path:
            # Convert file path format (remove curly braces if present)
            file_path = file_path.strip('{}')
            
            # Convert image
            success, result = ImageConverter.webp_to_png(file_path)
            
            if success:
                self.status_label.configure(
                    text=f"Converted: {os.path.basename(result)}"
                )
                messagebox.showinfo(
                    "Success",
                    f"Image converted successfully!\nSaved as: {result}"
                )
            else:
                self.status_label.configure(text="Error: " + result)
                messagebox.showerror("Error", result)
    
    def _handle_drag_enter(self, event):
        """Handle drag enter event"""
        self.drop_label.configure(text="Release to convert!")
        
    def _handle_drag_leave(self, event):
        """Handle drag leave event"""
        self.drop_label.configure(text="Drag and drop WebP files here") 