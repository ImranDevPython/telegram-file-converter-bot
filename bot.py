"""Telegram File Converter Bot."""

import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes, 
    ConversationHandler
)

from config.messages import MESSAGES
from config.keyboards import get_conversion_keyboard
from config.formats import SUPPORTED_FORMATS, import_converter
from utils import (
    get_file_info, 
    normalize_file_extension, 
    format_file_info,
    extract_format_from_button, 
    cleanup_files,
    ConversionError,
    FileSizeError,
    UnsupportedFormatError
)

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB in bytes
MAX_OUTPUT_SIZE = 50 * 1024 * 1024  # 50MB in bytes
TEMP_DIR = os.path.join(os.getcwd(), 'temp')

# Conversation states
UPLOAD, FORMAT_SELECTION = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(MESSAGES['welcome'])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(MESSAGES['help'])

async def handle_conversion_error(update: Update, error: Exception) -> None:
    """Handle conversion errors and send appropriate messages."""
    error_msg = str(error).lower()
    
    if isinstance(error, FileSizeError) or "too large" in error_msg:
        await update.message.reply_text(
            '⚠️ The converted file is too large to send via Telegram (>50MB).\n'
            'Please try with a smaller file or use a different format.'
        )
    elif isinstance(error, UnsupportedFormatError) or isinstance(error, ImportError):
        await update.message.reply_text(
            '❌ Sorry, this conversion is not supported.\n'
            'Please try a different format.'
        )
    elif isinstance(error, ConversionError):
        await update.message.reply_text(
            '❌ Sorry, there was an error converting your file.\n'
            'The file might be corrupted or in an unsupported format.\n'
            'Please try again with a different file.'
        )
    else:
        await update.message.reply_text(MESSAGES['error_generic'])
    
    logger.error(f"Conversion error: {str(error)}")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the uploaded file and show available conversion options."""
    try:
        # Get and store file information
        file_info = get_file_info(update)
        context.user_data.update(file_info)

        # Get file details
        file = await context.bot.get_file(file_info['file_id'])
        file_size = file.file_size
        file_ext = normalize_file_extension(file_info['file_name'])

        # Show file information
        await update.message.reply_text(
            format_file_info(file_info['file_name'], file_size, file_ext),
            reply_markup=ReplyKeyboardRemove()
        )

        # Validate file size
        if file_size > MAX_FILE_SIZE:
            await update.message.reply_text(MESSAGES['file_too_large'])
            return ConversationHandler.END

        # Validate file format
        if not file_info['is_photo'] and file_ext not in SUPPORTED_FORMATS:
            await update.message.reply_text(MESSAGES['unsupported_format'])
            return ConversationHandler.END

        # Show conversion options
        keyboard = get_conversion_keyboard(file_ext, file_info['is_photo'])
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            selective=True
        )
        await update.message.reply_text(MESSAGES['choose_format'], reply_markup=reply_markup)
        return FORMAT_SELECTION

    except Exception as e:
        logger.error(f"Error in handle_file: {str(e)}")
        await update.message.reply_text(MESSAGES['error_generic'])
        return ConversationHandler.END

async def convert_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Convert the file to the selected format."""
    output_path = None
    input_path = None
    progress_message = None
    
    try:
        selected_format = extract_format_from_button(update.message.text)
        
        if selected_format == 'cancel':
            await update.message.reply_text(
                '❌ Operation cancelled.\nSend me a new file when you\'re ready!',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        try:
            progress_message = await update.message.reply_text('📥 Downloading file...\nPlease wait.')
            
            # Setup and download
            file = await context.bot.get_file(context.user_data['file_id'])
            os.makedirs(TEMP_DIR, exist_ok=True)
            input_path = os.path.join(TEMP_DIR, context.user_data['file_name'])
            await file.download_to_drive(input_path)
            
            await progress_message.edit_text('🔄 Converting your file...\nThis might take a moment.')
            
            # Convert file
            input_format = normalize_file_extension(context.user_data['file_name'])
            original_filename = os.path.splitext(context.user_data['file_name'])[0]
            
            converter = import_converter(input_format, selected_format)
            if not converter:
                raise UnsupportedFormatError("Conversion not supported")
            
            output_path = (converter(input_path, selected_format) 
                         if selected_format in ['jpg', 'png'] 
                         else converter(input_path))
            
            if not output_path or not os.path.exists(output_path):
                raise ConversionError("Conversion failed")
            
            if os.path.getsize(output_path) > MAX_OUTPUT_SIZE:
                raise FileSizeError("Output file too large")
            
            # Send converted file
            await progress_message.edit_text('📤 Sending converted file...\nAlmost done!')
            
            new_filename = f"{original_filename}.{selected_format}"
            with open(output_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename=new_filename,
                    caption='✅ Here\'s your converted file!',
                    read_timeout=120,
                    write_timeout=120,
                    connect_timeout=60,
                    pool_timeout=60
                )
            
            await progress_message.delete()
            await update.message.reply_text(
                '✨ Send me another file to convert!',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
            
        except Exception as e:
            await handle_conversion_error(update, e)
            return ConversationHandler.END

    except Exception as e:
        logger.error(f"Error in convert_file: {str(e)}")
        await update.message.reply_text(MESSAGES['error_generic'])
        return ConversationHandler.END
        
    finally:
        await cleanup_files(input_path, output_path)
        if progress_message:
            try:
                await progress_message.delete()
            except:
                pass

def setup_handlers(application: Application) -> None:
    """Set up all handlers for the application."""
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file)],
        states={
            FORMAT_SELECTION: [
                MessageHandler(
                    filters.Regex('^(📄 Convert to PDF 📱|📄 Convert to PDF 📊|'
                                '🖼️ Convert to JPG 🎨|🖼️ Convert to PNG 🎨|'
                                '📊 Convert to XLSX 📈|📊 Convert to CSV 📉|'
                                '❌ Cancel ↩️|Convert another file 📤)$'),
                    convert_file
                )
            ],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)

def main() -> None:
    """Start the bot."""
    try:
        application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
        setup_handlers(application)
        logger.info("Starting bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        raise

if __name__ == '__main__':
    main()
