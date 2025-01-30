"""Keyboard configurations for the bot."""

from telegram import KeyboardButton
from config.formats import SUPPORTED_FORMATS

KEYBOARD_LAYOUTS = {
    'jpg': [
        [KeyboardButton('📄 Convert to PDF 📱')],
        [KeyboardButton('🖼️ Convert to PNG 🎨')]
    ],
    'jpeg': [
        [KeyboardButton('📄 Convert to PDF 📱')],
        [KeyboardButton('🖼️ Convert to PNG 🎨')]
    ],
    'png': [
        [KeyboardButton('📄 Convert to PDF 📱')],
        [KeyboardButton('🖼️ Convert to JPG 🎨')]
    ],
    'docx': [
        [KeyboardButton('📄 Convert to PDF 📱')]
    ],
    'csv': [
        [KeyboardButton('📄 Convert to PDF 📊')],
        [KeyboardButton('📊 Convert to XLSX 📈')]
    ],
    'xlsx': [
        [KeyboardButton('📊 Convert to CSV 📉')]
    ]
}

CANCEL_BUTTON = [KeyboardButton('❌ Cancel ↩️')]

def get_conversion_keyboard(file_ext, is_photo=False):
    """Get the appropriate keyboard layout for file conversion."""
    keyboard = []
    
    if is_photo:
        keyboard = [
            ['🖼️ Convert to JPG 🎨', '🖼️ Convert to PNG 🎨'],
            ['📄 Convert to PDF 📱']
        ]
    else:
        formats = SUPPORTED_FORMATS.get(file_ext, [])
        
        if 'pdf' in formats:
            keyboard.append(['📄 Convert to PDF 📱'])
        if 'xlsx' in formats:
            keyboard.append(['📊 Convert to XLSX 📈'])
        if 'csv' in formats:
            keyboard.append(['📊 Convert to CSV 📉'])
        if 'jpg' in formats:
            keyboard.append(['🖼️ Convert to JPG 🎨'])
        if 'png' in formats:
            keyboard.append(['🖼️ Convert to PNG 🎨'])
    
    # Always add exactly one cancel button at the end
    keyboard.append(['❌ Cancel ↩️'])
    
    return keyboard 