import base64
from io import BytesIO
from PIL import Image
from typing import List, Tuple
from fastapi import UploadFile, HTTPException
from config import config

class ImageProcessor:
    @staticmethod
    async def validate_image(file: UploadFile) -> None:
        """Validate uploaded image"""
        # Check file extension
        file_ext = f".{file.filename.split('.')[-1].lower()}"
        if file_ext not in config.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > config.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {config.MAX_IMAGE_SIZE / (1024*1024)}MB"
            )
        
        # Reset file pointer
        await file.seek(0)
    
    @staticmethod
    async def image_to_base64(file: UploadFile) -> Tuple[str, str]:
        """Convert uploaded image to base64 string"""
        content = await file.read()
        
        # Open image to verify it's valid
        try:
            image = Image.open(BytesIO(content))
            image.verify()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(e)}"
            )
        
        # Get image format
        await file.seek(0)
        image = Image.open(BytesIO(content))
        image_format = image.format.lower()
        
        # Convert to base64
        base64_image = base64.b64encode(content).decode('utf-8')
        
        return base64_image, image_format
    
    @staticmethod
    async def process_multiple_images(files: List[UploadFile]) -> List[Tuple[str, str, str]]:
        """Process multiple images and return list of (filename, base64, format)"""
        processed_images = []
        
        for file in files:
            await ImageProcessor.validate_image(file)
            base64_data, img_format = await ImageProcessor.image_to_base64(file)
            processed_images.append((file.filename, base64_data, img_format))
        
        return processed_images