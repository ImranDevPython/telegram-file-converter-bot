"""Keyboard configurations for the bot."""

from telegram import KeyboardButton

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

def get_conversion_keyboard(file_ext: str, is_photo: bool = False) -> list:
    """Get the appropriate keyboard layout based on file type."""
    keyboard = KEYBOARD_LAYOUTS.get(file_ext, []) if not is_photo else KEYBOARD_LAYOUTS['jpg']
    keyboard.append(CANCEL_BUTTON)
    return keyboard 