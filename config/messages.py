"""Message templates for the bot."""

MESSAGES = {
    'welcome': (
        'Welcome to the File Converter Bot! 👋\n\n'
        'I can help you convert files between different formats.\n\n'
        '📝 Available Conversions:\n\n'
        '📄 Documents:\n'
        '• DOCX → PDF\n\n'
        '📊 Spreadsheets:\n'
        '• CSV → PDF (Tables)\n'
        '• CSV → XLSX (Excel)\n'
        '• XLSX → CSV\n\n'
        '🖼️ Images:\n'
        '• JPG → PDF\n'
        '• JPG → PNG\n'
        '• PNG → PDF\n'
        '• PNG → JPG\n\n'
        'Just send me a file and I\'ll show you the available conversion options!'
    ),
    'help': (
        'Here\'s how to use me:\n\n'
        '1️⃣ Send me a file\n'
        '2️⃣ Choose the format you want to convert to\n'
        '3️⃣ Wait for the converted file\n\n'
        '📝 Supported Formats:\n\n'
        '📄 Documents:\n'
        '• DOCX → PDF\n\n'
        '📊 Spreadsheets:\n'
        '• CSV → PDF (Tables)\n'
        '• CSV → XLSX (Excel)\n'
        '• XLSX → CSV\n\n'
        '🖼️ Images:\n'
        '• JPG → PDF\n'
        '• JPG → PNG\n'
        '• PNG → PDF\n'
        '• PNG → JPG\n\n'
        '❗ Maximum file size: 20MB\n'
        '❓ Need help? Contact @YourUsername'
    ),
    'file_too_large': (
        '❌ File is too large! Maximum size is 20MB.\n'
        'Please compress your file and try again.\n\n'
        '💡 Tips:\n'
        '• Compress the file\n'
        '• Split it into smaller parts\n'
        '• Use a different format'
    ),
    'unsupported_format': (
        '✅ I can handle these formats:\n'
        '📄 Documents: DOCX\n'
        '📊 Spreadsheets: CSV, XLSX\n'
        '🖼️ Images: JPG, JPEG, PNG\n\n'
        '💡 Tip: Make sure your file has the correct extension!'
    ),
    'choose_format': (
        '✨ Choose your conversion format:\n'
        'Tap the grid icon 🔲 below'
    ),
    'error_generic': (
        '❌ Sorry, something went wrong.\n'
        'Please try again or contact support if the problem persists.\n\n'
        '💡 Make sure:\n'
        '• The file isn\'t corrupted\n'
        '• The file extension matches its content\n'
        '• You have a stable internet connection'
    )
} 