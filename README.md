# Telegram File Converter Bot

A Telegram bot that converts files between various formats including PDF, DOCX, and images.

## Features

- Convert PDF to Word (DOCX)
- Convert images (JPG, PNG) to PDF
- Convert Word (DOCX) to PDF
- Error handling and logging
- User-friendly interface

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Telegram Bot Token:
```
BOT_TOKEN=your_bot_token_here
```

5. Run the bot:
```bash
python bot.py
```

## Supported Conversions

- PDF → DOCX
- DOCX → PDF
- JPG/PNG → PDF

## Project Structure

```
file_converter_bot/
├── bot.py                  # Main bot script
├── converters/             # Conversion logic
├── utils/                  # Utility functions
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Versioning
This project uses [Semantic Versioning](https://semver.org/). Current version: `1.0.0`
