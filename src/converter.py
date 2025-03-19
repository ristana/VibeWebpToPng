from PIL import Image
import os
from typing import Tuple

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