# Telegram File Converter Bot

A Telegram bot that can convert files between different formats.

## Supported Conversions

- 📄 DOCX → PDF
- 🖼️ Images (JPG/PNG) → PDF
- 🔄 JPG ↔️ PNG

## Setup

1. Clone the repository
```bash
git clone <your-repo-url>
cd Telegram-file-converter-bot
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your bot token:
```
BOT_TOKEN=your_bot_token_here
```

5. Run the bot
```bash
python bot.py
```

## Features

- Convert DOCX files to PDF
- Convert images (JPG/PNG) to PDF
- Convert between JPG and PNG formats
- Progress updates during conversion
- File size limit: 20MB
- High-quality image conversion

## Version History

- v1.0.0 - Initial release
  - Basic file conversion functionality
  - Support for DOCX, PDF, JPG, and PNG formats
  - Progress messages during conversion
  - File size limits and error handling

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
