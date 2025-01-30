"""Utility functions for the bot."""

import os
import logging
from typing import Dict, Union
from telegram import Update

logger = logging.getLogger(__name__)

# Type aliases
FileInfo = Dict[str, Union[bool, str]]

def get_file_info(update: Update) -> FileInfo:
    """Extract file information from the update."""
    if update.message.photo:
        return {
            'is_photo': True,
            'file_id': update.message.photo[-1].file_id,
            'file_name': 'photo.jpg'
        }
    return {
        'is_photo': False,
        'file_id': update.message.document.file_id,
        'file_name': update.message.document.file_name
    }

def normalize_file_extension(file_name: str) -> str:
    """Get and normalize file extension."""
    ext = os.path.splitext(file_name)[1][1:].lower()
    return 'jpg' if ext == 'jpeg' else ext

def format_file_info(file_name: str, file_size: int, file_ext: str) -> str:
    """Format file information message."""
    size_mb = round(file_size / (1024 * 1024), 2)
    return (
        f'📁 File Information:\n'
        f'📝 Name: {file_name}\n'
        f'📊 Size: {size_mb} MB\n'
        f'🏷️ Type: {file_ext.upper()}'
    )

def extract_format_from_button(button_text: str) -> str:
    """Extract format from button text."""
    return (button_text.lower()
        .replace('📄 convert to ', '')
        .replace('🖼️ convert to ', '')
        .replace(' convert to ', '')
        .replace(' 📱', '')
        .replace(' 🎨', '')
        .replace(' 📈', '')
        .replace(' 📉', '')
        .replace(' 📊', '')
        .replace(' ↩️', ''))

async def cleanup_files(*paths: str) -> None:
    """Clean up temporary files."""
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                logger.error(f"Cleanup error: {str(e)}")

# Custom exceptions
class ConversionError(Exception):
    """Base exception for conversion errors."""
    pass

class FileSizeError(ConversionError):
    """Exception raised when file size exceeds limits."""
    pass

class UnsupportedFormatError(ConversionError):
    """Exception raised for unsupported format conversions."""
    pass

# Export all functions and classes
__all__ = [
    'get_file_info',
    'normalize_file_extension',
    'format_file_info',
    'extract_format_from_button',
    'cleanup_files',
    'ConversionError',
    'FileSizeError',
    'UnsupportedFormatError'
]
