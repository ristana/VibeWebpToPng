from PIL import Image
import os
from typing import Tuple, List, Callable
from queue import Queue
from threading import Thread
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ConversionResult:
    """Represents the result of a single file conversion"""
    success: bool
    input_path: str
    output_path: str
    error_message: str = ""

class ConversionQueue:
    """Manages batch conversion of WebP files"""
    def __init__(self, 
                 on_file_complete: Callable[[ConversionResult], None],
                 on_batch_progress: Callable[[int, int], None]):
        self.queue: Queue = Queue()
        self.on_file_complete = on_file_complete
        self.on_batch_progress = on_batch_progress
        self.total_files = 0
        self.completed_files = 0
        self.is_processing = False
        self._worker_thread = None
        self._should_stop = False
        self.completed_results: List[ConversionResult] = []

    def add_files(self, file_paths: List[str]) -> None:
        """Add files to the conversion queue"""
        # Stop current processing if any
        self._should_stop = True
        if self._worker_thread and self._worker_thread.is_alive():
            self.queue.join()  # Wait for current processing to finish
            self._worker_thread.join(timeout=1.0)  # Wait for thread to end
        
        # Reset flags and counters
        self._should_stop = False
        self.is_processing = False
        self.total_files = 0
        self.completed_files = 0
        self.completed_results = []  # Reset completed results
        
        # Clear queue
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
                self.queue.task_done()
            except:
                pass
            
        # Add new files
        for path in file_paths:
            self.queue.put(path)
        self.total_files = len(file_paths)
        
        # Start processing
        self._start_processing()

    def _start_processing(self) -> None:
        """Start processing the queue in a background thread"""
        self.is_processing = True
        self._worker_thread = Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()

    def _process_queue(self) -> None:
        """Process files in the queue"""
        while not self.queue.empty() and not self._should_stop:
            input_path = self.queue.get()
            result = ImageConverter.webp_to_png(input_path)
            
            # Create conversion result
            if result[0]:  # Success
                conv_result = ConversionResult(
                    success=True,
                    input_path=input_path,
                    output_path=result[1]
                )
            else:  # Error
                conv_result = ConversionResult(
                    success=False,
                    input_path=input_path,
                    output_path="",
                    error_message=result[1]
                )
            
            # Store result and update progress
            self.completed_results.append(conv_result)
            self.completed_files += 1
            self.on_batch_progress(self.completed_files, self.total_files)
            self.on_file_complete(conv_result)
            
            self.queue.task_done()
        
        self.is_processing = False

class ImageConverter:
    @staticmethod
    def webp_to_png(input_path: str) -> Tuple[bool, str]:
        """
        Convert a WebP image to PNG format
        
        Args:
            input_path (str): Path to the input WebP file
            
        Returns:
            Tuple[bool, str]: (Success status, Message or output path)
        """
        try:
            # Validate input file exists
            if not os.path.exists(input_path):
                return False, "Input file does not exist"
                
            # Validate input file is WebP
            if not input_path.lower().endswith('.webp'):
                return False, "Input file is not a WebP image"
            
            # Generate output path
            output_path = os.path.splitext(input_path)[0] + '.png'
            
            # Open and convert image
            with Image.open(input_path) as image:
                image.save(output_path, 'PNG')
            
            return True, output_path
            
        except Exception as e:
            return False, f"Error converting image: {str(e)}" 