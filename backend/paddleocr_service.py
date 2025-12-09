"""
PaddleOCR-VL integration for manga speech bubble detection and text extraction
"""
from paddleocr import PaddleOCR
from PIL import Image
from io import BytesIO
import requests
import numpy as np
from typing import List, Dict

class MangaOCR:
    def __init__(self):
        # Initialize PaddleOCR with Japanese support
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='japan',
            use_gpu=False
        )

    def extract_from_url(self, image_url: str) -> List[Dict]:
        """
        Extract text and bounding boxes from manga image URL
        """
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            
            # Convert PIL Image to numpy array for PaddleOCR
            import numpy as np
            img_array = np.array(img)
            
        except Exception as e:
            print(f"[OCR] Failed to load image: {e}")
            return []

        result = self.ocr.ocr(img_array, cls=True)
        
        # Handle empty results
        if not result or not result[0]:
            print("[OCR] No text detected in image")
            return []
        
        bubbles = []

        for line in result[0]:
            box = line[0]
            text = line[1][0]
            confidence = line[1][1]

            x_coords = [point[0] for point in box]
            y_coords = [point[1] for point in box]

            x = int(min(x_coords))
            y = int(min(y_coords))
            width = int(max(x_coords) - x)
            height = int(max(y_coords) - y)

            # Only include high-confidence detections
            if confidence > 0.5:
                bubbles.append({
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "text": text,
                    "confidence": confidence
                })
            else:
                print(f"[OCR] Skipped low confidence text: {text} ({confidence:.2f})")

        return bubbles

# Singleton
manga_ocr = MangaOCR()
