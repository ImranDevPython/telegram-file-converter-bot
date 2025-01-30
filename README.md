# Telegram File Converter Bot

A versatile Telegram bot that helps users convert files between different formats. The bot supports various file types including documents, images, and spreadsheets.

## Features

- 📄 **Document Conversion**
  - DOCX → PDF

- 📊 **Spreadsheet Conversion**
  - CSV → PDF (Tables)
  - CSV → XLSX (Excel)
  - XLSX → CSV

- 🖼️ **Image Conversion**
  - JPG/JPEG → PDF
  - JPG/JPEG → PNG
  - PNG → PDF
  - PNG → JPG

## Technical Details

- Built with Python 3.x and python-telegram-bot
- Modular architecture with separate configuration and utility modules
- Robust error handling and user feedback
- File size limits:
  - Input files: 20MB
  - Output files: 50MB

## Project Structure

```
telegram-file-converter-bot/
├── bot.py                 # Main bot file
├── config/               # Configuration modules
│   ├── __init__.py
│   ├── formats.py        # Format configurations
│   ├── keyboards.py      # Keyboard layouts
│   └── messages.py       # Message templates
├── converters/           # File conversion modules
│   ├── __init__.py
│   ├── csv_to_pdf.py
│   ├── csv_to_xlsx.py
│   ├── docx_to_pdf.py
│   ├── image_converter.py
│   ├── image_to_pdf.py
│   └── xlsx_to_csv.py
├── utils/               # Utility functions
│   └── __init__.py      # File handling and helpers
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ImranDevPython/telegram-file-converter-bot.git
   cd telegram-file-converter-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix or MacOS:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Telegram Bot Token:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

5. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Start a chat with the bot on Telegram
2. Send `/start` to get an introduction
3. Send a file you want to convert
4. Choose the desired output format from the provided options
5. Wait for the converted file

## Error Handling

The bot includes comprehensive error handling for:
- File size limits
- Unsupported formats
- Conversion failures
- Network issues
- Invalid files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the Telegram Bot API wrapper
- Various Python libraries used for file conversion
