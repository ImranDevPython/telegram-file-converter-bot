import os
import tempfile
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.enums import TA_CENTER

def convert_csv_to_pdf(csv_path: str) -> str:
    """
    Convert CSV file to PDF with formatted tables
    Args:
        csv_path (str): Path to the CSV file
    Returns:
        str: Path to the converted PDF file
    """
    try:
        # Create temporary file for PDF
        temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_pdf.close()

        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            temp_pdf.name,
            pagesize=landscape(letter),
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        
        # Create styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        # Create the elements to build the PDF
        elements = []
        
        # Add title (using the CSV filename as title)
        title = os.path.splitext(os.path.basename(csv_path))[0]
        title = title.replace('_', ' ').replace('-', ' ').title()
        elements.append(Paragraph(title, title_style))
        
        # Prepare table data
        table_data = [df.columns.tolist()] + df.values.tolist()
        
        # Create table
        table = Table(table_data)
        
        # Add style to table
        style = TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Data style
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        
        # Add table to elements
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        return temp_pdf.name
        
    except Exception as e:
        if os.path.exists(temp_pdf.name):
            os.remove(temp_pdf.name)
        raise Exception(f"Error converting CSV to PDF: {str(e)}") 