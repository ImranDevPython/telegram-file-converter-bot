"""Format configurations and converter imports."""

from typing import Optional, Callable, Dict, List
import logging

logger = logging.getLogger(__name__)

# Type aliases
ConverterFunction = Callable[[str, Optional[str]], str]

# Supported formats
SUPPORTED_FORMATS: Dict[str, List[str]] = {
    'docx': ['pdf'],
    'jpg': ['pdf', 'png'],
    'jpeg': ['pdf', 'png'],
    'png': ['pdf', 'jpg'],
    'csv': ['pdf', 'xlsx'],
    'xlsx': ['csv']
}

def import_converter(from_format: str, to_format: str) -> Optional[ConverterFunction]:
    """Import the appropriate converter based on formats."""
    try:
        if from_format in ['jpg', 'jpeg', 'png']:
            if to_format == 'pdf':
                from converters.image_to_pdf import convert_image_to_pdf
                return convert_image_to_pdf
            elif to_format in ['jpg', 'png']:
                from converters.image_converter import convert_image
                return convert_image
        elif from_format == 'docx' and to_format == 'pdf':
            from converters.docx_to_pdf import convert_docx_to_pdf
            return convert_docx_to_pdf
        elif from_format == 'csv':
            if to_format == 'pdf':
                from converters.csv_to_pdf import convert_csv_to_pdf
                return convert_csv_to_pdf
            elif to_format == 'xlsx':
                from converters.csv_to_xlsx import convert_csv_to_xlsx
                return convert_csv_to_xlsx
        elif from_format == 'xlsx' and to_format == 'csv':
            from converters.xlsx_to_csv import convert_xlsx_to_csv
            return convert_xlsx_to_csv
        return None
    except ImportError as e:
        logger.error(f"Import error in import_converter: {str(e)}")
        return None 