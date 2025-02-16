# Telegram File Converter Bot

A versatile Telegram bot that helps users convert files between different formats. The bot supports various file types including documents, images, and spreadsheets.

## Features

- 📊 **Spreadsheet Conversion**
  - CSV → PDF (Tables)
  - CSV → XLSX (Excel)
  - XLSX → CSV

- 🖼️ **Image Conversion**
  - JPG/JPEG → PDF
  - JPG/JPEG → PNG
  - PNG → PDF
  - PNG → JPG

## How to Use This Bot

### Option 1: Use the Existing Bot
1. Open Telegram
2. Search for `@QConvertBot`
3. Start a chat with the bot
4. Send `/start` to begin
5. Send any supported file
6. Choose the conversion format from the provided options
7. Wait for your converted file

### Option 2: Host Your Own Bot

If you want to run your own instance of this bot:

1. Clone this repository:
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

4. Create a new bot on Telegram:
   - Open Telegram
   - Search for `@BotFather`
   - Send `/newbot`
   - Follow the instructions to create your bot
   - Copy the API token provided

5. Create a `.env` file in the project root:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

6. Run the bot:
   ```bash
   python bot.py
   ```

## File Size Limits
- Maximum input file size: 20MB
- Maximum output file size: 50MB

## Supported File Formats
- Documents: DOCX, PDF
- Images: JPG/JPEG, PNG
- Spreadsheets: CSV, XLSX

## Troubleshooting

Common issues and solutions:

1. **File Too Large**: Try compressing your file before uploading
2. **Conversion Failed**: Make sure your file is not corrupted and in the correct format
3. **Bot Not Responding**: Check if the bot is running and has proper internet connection

## Support

If you encounter any issues:
1. Check the [Issues](https://github.com/ImranDevPython/telegram-file-converter-bot/issues) section
2. Create a new issue if your problem isn't already reported

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Technical Details

- Built with Python 3.x and python-telegram-bot
- Modular architecture with separate configuration and utility modules
- Robust error handling and user feedback



## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the Telegram Bot API wrapper
- Various Python libraries used for file conversion
