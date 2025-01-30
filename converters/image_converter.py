from PIL import Image
import logging
import os

MAX_DIMENSION = 1920  # Maximum width or height for images
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB - Telegram's file size limit

def resize_if_needed(img: Image.Image) -> Image.Image:
    """Resize image if it exceeds maximum dimensions."""
    width, height = img.size
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        # Calculate aspect ratio
        aspect_ratio = width / height
        if width > height:
            new_width = MAX_DIMENSION
            new_height = int(MAX_DIMENSION / aspect_ratio)
        else:
            new_height = MAX_DIMENSION
            new_width = int(MAX_DIMENSION * aspect_ratio)
        
        logging.info(f"Resizing image from {width}x{height} to {new_width}x{new_height}")
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img

def convert_image(input_path: str, output_format: str) -> str:
    """
    Convert image between JPG and PNG formats
    Args:
        input_path (str): Path to input image file
        output_format (str): Target format ('jpg' or 'png')
    Returns:
        str: Path to the converted image file
    """
    output_path = None
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        # Open the image
        with Image.open(input_path) as img:
            # Log image details for debugging
            logging.info(f"Converting image: mode={img.mode}, size={img.size}, format={img.format}")
            
            # Resize image if too large
            img = resize_if_needed(img)
            
            # If image is in RGBA mode and converting to JPG, convert to RGB first
            if img.mode == 'RGBA' and output_format.lower() == 'jpg':
                img = img.convert('RGB')
                logging.info("Converted RGBA to RGB for JPG output")
            
            # Create output path
            output_path = input_path.rsplit('.', 1)[0] + '.' + output_format.lower()
            
            # Save with optimal settings
            if output_format.lower() == 'jpg':
                # Try different quality settings to get optimal file size
                quality = 95
                while quality > 60:  # Don't go below quality 60
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                    if os.path.getsize(output_path) <= MAX_FILE_SIZE:  
                        break
                    quality -= 5
            else:  # PNG
                # For PNG, use maximum compression
                img.save(output_path, 'PNG', optimize=True, compress_level=9)
            
            # Verify the output file was created
            if not os.path.exists(output_path):
                raise Exception("Output file was not created")
                
            if os.path.getsize(output_path) == 0:
                raise Exception("Output file is empty")
                
            # Check if file size is within Telegram's limit
            if os.path.getsize(output_path) > MAX_FILE_SIZE:
                raise Exception("Converted file exceeds Telegram's size limit")
                
            logging.info(f"Successfully converted image to {output_format}")
            return output_path
            
    except Exception as e:
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        logging.error(f"Error converting image: {str(e)}")
        raise Exception(f"Error converting image: {str(e)}")
