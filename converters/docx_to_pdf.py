from docx2pdf import convert
import tempfile
import os
import logging

def convert_docx_to_pdf(docx_path: str) -> str:
    """
    Convert DOCX to PDF format using docx2pdf
    Args:
        docx_path (str): Path to the DOCX file
    Returns:
        str: Path to the converted PDF file
    """
    output_path = None
    try:
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"DOCX file not found: {docx_path}")

        # Create output PDF path
        output_path = docx_path.rsplit('.', 1)[0] + '.pdf'
        
        # Convert DOCX to PDF
        convert(docx_path, output_path)
        
        # Verify the output file
        if not os.path.exists(output_path):
            raise Exception("Output file was not created")
            
        if os.path.getsize(output_path) == 0:
            raise Exception("Output file is empty")
            
        logging.info(f"Successfully converted DOCX to PDF")
        return output_path
        
    except Exception as e:
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        logging.error(f"Error converting DOCX to PDF: {str(e)}")
        raise Exception(f"Error converting DOCX to PDF: {str(e)}")
