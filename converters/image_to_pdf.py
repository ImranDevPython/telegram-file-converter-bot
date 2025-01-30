import os
import tempfile
from PIL import Image
import img2pdf

def convert_image_to_pdf(image_path: str) -> str:
    """
    Convert image (JPG/PNG) to PDF format
    Args:
        image_path (str): Path to the image file
    Returns:
        str: Path to the converted PDF file
    """
    try:
        # Create a temporary file for the output
        temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_pdf.close()
        
        # Open and convert image if needed
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[3])
                else:
                    rgb_img.paste(img, mask=img.split()[1])
                
                # Save as temporary PNG
                temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                rgb_img.save(temp_img.name, 'PNG')
                temp_img.close()
                
                # Convert to PDF
                with open(temp_img.name, 'rb') as img_file:
                    with open(temp_pdf.name, 'wb') as pdf_file:
                        pdf_file.write(img2pdf.convert(img_file))
                
                # Clean up temporary image
                os.remove(temp_img.name)
            else:
                # Convert directly to PDF
                with open(image_path, 'rb') as img_file:
                    with open(temp_pdf.name, 'wb') as pdf_file:
                        pdf_file.write(img2pdf.convert(img_file))
        
        return temp_pdf.name
        
    except Exception as e:
        if os.path.exists(temp_pdf.name):
            os.remove(temp_pdf.name)
        raise Exception(f"Error converting image to PDF: {str(e)}")
