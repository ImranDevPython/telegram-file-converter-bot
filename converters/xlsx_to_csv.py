import os
import tempfile
import pandas as pd

def convert_xlsx_to_csv(xlsx_path: str) -> str:
    """
    Convert XLSX file to CSV format
    Args:
        xlsx_path (str): Path to the XLSX file
    Returns:
        str: Path to the converted CSV file
    """
    try:
        # Create temporary file for CSV
        temp_csv = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        temp_csv.close()

        # Read Excel file
        # Use openpyxl engine for better compatibility
        df = pd.read_excel(xlsx_path, engine='openpyxl')
        
        # Convert to CSV with proper encoding and handling
        df.to_csv(
            temp_csv.name,
            index=False,  # Don't include row numbers
            encoding='utf-8-sig',  # Use UTF-8 with BOM for Excel compatibility
            quoting=1,  # Quote all non-numeric values
            escapechar='\\',  # Use backslash as escape character
            date_format='%Y-%m-%d',  # ISO date format
            float_format='%.6f'  # 6 decimal places for floats
        )
        
        return temp_csv.name
        
    except Exception as e:
        if os.path.exists(temp_csv.name):
            os.remove(temp_csv.name)
        raise Exception(f"Error converting XLSX to CSV: {str(e)}") 