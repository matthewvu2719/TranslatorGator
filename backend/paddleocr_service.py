"""
PaddleOCR-VL integration for speech bubble detection and text extraction
"""
from paddleocr import PaddleOCR
import requests
from PIL import Image
from io import BytesIO
from typing import List, Tuple

class MangaOCR:
    def __init__(self):
        # Initialize PaddleOCR with Japanese support
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='japan',  # Support for Japanese
            use_gpu=False  # Set to True if GPU available
        )
    
    def extract_from_url(self, image_url: str) -> List[dict]:
        """
        Extract text and bounding boxes from manga image URL
        """
        # Download image
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Run OCR
        result = self.ocr.ocr(img, cls=True)
        
        bubbles = []
        for line in result[0]:
            box = line[0]  # Bounding box coordinates
            text = line[1][0]  # Extracted text
            confidence = line[1][1]  # Confidence score
            
            # Convert box to x, y, width, height
            x_coords = [point[0] for point in box]
            y_coords = [point[1] for point in box]
            
            x = int(min(x_coords))
            y = int(min(y_coords))
            width = int(max(x_coords) - x)
            height = int(max(y_coords) - y)
            
            bubbles.append({
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'text': text,
                'confidence': confidence
            })
        
        return bubbles

# Singleton instance
manga_ocr = MangaOCR()
