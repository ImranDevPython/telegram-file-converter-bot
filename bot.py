import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import tempfile

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
UPLOAD, FORMAT_SELECTION = range(2)

# Supported formats and their possible conversions
SUPPORTED_FORMATS = {
    'docx': ['pdf'],
    'jpg': ['pdf', 'png'],
    'jpeg': ['pdf', 'png'],
    'png': ['pdf', 'jpg'],
    'csv': ['pdf', 'xlsx'],
    'xlsx': ['csv']
}

# Import converters
def import_converter(from_format: str, to_format: str):
    """Import the appropriate converter based on formats."""
    try:
        if from_format in ['jpg', 'jpeg', 'png']:
            if to_format == 'pdf':
                from converters.image_to_pdf import convert_image_to_pdf
                return convert_image_to_pdf
            elif to_format in ['jpg', 'png']:
                from converters.image_converter import convert_image
                return convert_image
        elif from_format == 'docx' and to_format == 'pdf':
            from converters.docx_to_pdf import convert_docx_to_pdf
            return convert_docx_to_pdf
        elif from_format == 'csv':
            if to_format == 'pdf':
                from converters.csv_to_pdf import convert_csv_to_pdf
                return convert_csv_to_pdf
            elif to_format == 'xlsx':
                from converters.csv_to_xlsx import convert_csv_to_xlsx
                return convert_csv_to_xlsx
        elif from_format == 'xlsx' and to_format == 'csv':
            from converters.xlsx_to_csv import convert_xlsx_to_csv
            return convert_xlsx_to_csv
        return None
    except ImportError as e:
        logging.error(f"Import error in import_converter: {str(e)}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
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
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
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
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the uploaded file and show available conversion options."""
    try:
        # Check if it's a photo
        if update.message.photo:
            context.user_data['is_photo'] = True
            context.user_data['file_id'] = update.message.photo[-1].file_id
            context.user_data['file_name'] = 'photo.jpg'
        else:
            context.user_data['is_photo'] = False
            context.user_data['file_id'] = update.message.document.file_id
            context.user_data['file_name'] = update.message.document.file_name

        # Get file info
        file = await context.bot.get_file(context.user_data['file_id'])
        file_size = file.file_size
        file_ext = os.path.splitext(context.user_data['file_name'])[1][1:].lower()
        if file_ext == 'jpeg':
            file_ext = 'jpg'

        # Show file information with keyboard removal first
        size_mb = round(file_size / (1024 * 1024), 2)
        await update.message.reply_text(
            f'📁 File Information:\n'
            f'📝 Name: {context.user_data["file_name"]}\n'
            f'📊 Size: {size_mb} MB\n'
            f'🏷️ Type: {file_ext.upper()}',
            reply_markup=ReplyKeyboardRemove()
        )

        # Check file size (20MB limit)
        if file_size > 20 * 1024 * 1024:
            await update.message.reply_text(
                '❌ File is too large! Maximum size is 20MB.\n'
                'Please compress your file and try again.\n\n'
                '💡 Tips:\n'
                '• Compress the file\n'
                '• Split it into smaller parts\n'
                '• Use a different format'
            )
            return ConversationHandler.END

        # Check if file format is supported
        if not context.user_data.get('is_photo', False) and file_ext not in SUPPORTED_FORMATS:
            await update.message.reply_text(
                f'❌ Sorry, I don\'t support {file_ext.upper()} files.\n\n'
                '✅ I can handle these formats:\n'
                '📄 Documents: DOCX\n'
                '📊 Spreadsheets: CSV, XLSX\n'
                '🖼️ Images: JPG, JPEG, PNG\n\n'
                '💡 Tip: Make sure your file has the correct extension!'
            )
            return ConversationHandler.END

        # Show conversion options with improved keyboard layout
        keyboard = []
        if context.user_data.get('is_photo', False) or file_ext in ['jpg', 'jpeg']:
            keyboard = [
                [KeyboardButton('📄 Convert to PDF 📱')],
                [KeyboardButton('🖼️ Convert to PNG 🎨')],
                [KeyboardButton('❌ Cancel ↩️')]
            ]
        elif file_ext == 'png':
            keyboard = [
                [KeyboardButton('📄 Convert to PDF 📱')],
                [KeyboardButton('🖼️ Convert to JPG 🎨')],
                [KeyboardButton('❌ Cancel ↩️')]
            ]
        elif file_ext == 'docx':
            keyboard = [
                [KeyboardButton('📄 Convert to PDF 📱')],
                [KeyboardButton('❌ Cancel ↩️')]
            ]
        elif file_ext == 'csv':
            keyboard = [
                [KeyboardButton('📄 Convert to PDF 📊')],
                [KeyboardButton('📊 Convert to XLSX 📈')],
                [KeyboardButton('❌ Cancel ↩️')]
            ]
        elif file_ext == 'xlsx':
            keyboard = [
                [KeyboardButton('📊 Convert to CSV 📉')],
                [KeyboardButton('❌ Cancel ↩️')]
            ]

        # Create keyboard markup with mobile-friendly settings
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,  # Keep keyboard visible
            selective=True  # Show keyboard only to the user who triggered the command
        )

        # Show the keyboard with instructions in a single message
        await update.message.reply_text(
            '✨ Choose your conversion format:\n'
            'Tap the grid icon 🔲 below',
            reply_markup=reply_markup
        )

        return FORMAT_SELECTION

    except Exception as e:
        logging.error(f"Error in handle_file: {str(e)}")
        await update.message.reply_text(
            '❌ Sorry, something went wrong while processing your file.\n'
            'Please try again or contact support if the problem persists.\n\n'
            '💡 Make sure:\n'
            '• The file isn\'t corrupted\n'
            '• The file extension matches its content\n'
            '• You have a stable internet connection'
        )
        return ConversationHandler.END

async def convert_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Convert the file to the selected format."""
    output_path = None
    input_path = None
    progress_message = None
    try:
        # Get the selected format (remove emoji and text)
        selected_format = update.message.text.lower()
        selected_format = selected_format.replace('📄 convert to ', '')
        selected_format = selected_format.replace('🖼️ convert to ', '')
        selected_format = selected_format.replace(' convert to ', '')
        selected_format = selected_format.replace(' 📱', '')
        selected_format = selected_format.replace(' 🎨', '')
        selected_format = selected_format.replace(' 📈', '')
        selected_format = selected_format.replace(' 📉', '')
        selected_format = selected_format.replace(' 📊', '')
        selected_format = selected_format.replace(' ↩️', '')
        
        # Check if user wants to cancel
        if selected_format.lower() == 'cancel':
            # Use ReplyKeyboardRemove to hide the keyboard
            await update.message.reply_text(
                '❌ Operation cancelled.\n'
                'Send me a new file when you\'re ready!',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
        
        # Send initial progress message
        progress_message = await update.message.reply_text(
            '📥 Downloading file...\n'
            'Please wait.'
        )
        
        # Download the file
        file = await context.bot.get_file(context.user_data['file_id'])
        
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Download to temp file with timeout
        input_path = os.path.join(temp_dir, context.user_data['file_name'])
        await file.download_to_drive(input_path)
        
        # Update progress for conversion
        await progress_message.edit_text(
            '🔄 Converting your file...\n'
            'This might take a moment, please wait.'
        )
        
        try:
            # Get input format and original filename without extension
            input_format = os.path.splitext(context.user_data['file_name'])[1][1:].lower()
            original_filename = os.path.splitext(context.user_data['file_name'])[0]
            if input_format == 'jpeg':
                input_format = 'jpg'
            
            # Import appropriate converter
            converter = import_converter(input_format, selected_format.lower())
            if converter is None:
                await update.message.reply_text(
                    '❌ Sorry, this conversion is not supported.\n'
                    'Please try a different format.'
                )
                return ConversationHandler.END
                
            # Convert the file
            if selected_format.lower() in ['jpg', 'png']:
                output_path = converter(input_path, selected_format.lower())
            else:
                output_path = converter(input_path)
            
            if not output_path or not os.path.exists(output_path):
                raise Exception("Conversion failed to produce output file")
            
            # Check file size
            file_size = os.path.getsize(output_path)
            if file_size > 50 * 1024 * 1024:  # If larger than 50MB
                await update.message.reply_text(
                    '⚠️ The converted file is too large to send via Telegram (>50MB).\n'
                    'Please try with a smaller file or use a different format.'
                )
                return ConversationHandler.END
            
            # Update progress for sending
            await progress_message.edit_text(
                '📤 Sending converted file...\n'
                'Almost done!'
            )
            
            # Send the converted file with appropriate timeouts
            try:
                with open(output_path, 'rb') as f:
                    # Use original filename with new extension
                    new_filename = f"{original_filename}.{selected_format.lower()}"
                    await update.message.reply_document(
                        document=f,
                        filename=new_filename,
                        caption='✅ Here\'s your converted file!',
                        read_timeout=120,  # 2 minutes
                        write_timeout=120,  # 2 minutes
                        connect_timeout=60,
                        pool_timeout=60
                    )
                
                # Delete progress message
                await progress_message.delete()
                
                # Simple completion message
                await update.message.reply_text(
                    '✨ Send me another file to convert!',
                    reply_markup=ReplyKeyboardRemove()
                )
                
            except Exception as e:
                if "Request Entity Too Large" in str(e):
                    await update.message.reply_text(
                        '⚠️ The converted file is too large to send via Telegram.\n'
                        'Try splitting it into smaller parts or use a different format.'
                    )
                elif "Timed out" in str(e):
                    await update.message.reply_text(
                        '⚠️ The file took too long to send.\n'
                        'Please try with a smaller file.'
                    )
                else:
                    raise e
                    
            return ConversationHandler.END

        except ImportError as e:
            logging.error(f"Import error during conversion: {str(e)}")
            await update.message.reply_text(
                '❌ This conversion type is currently not available.\n'
                'Please try a different format.'
            )
            return ConversationHandler.END
        except Exception as e:
            logging.error(f"Error during conversion: {str(e)}")
            await update.message.reply_text(
                '❌ Sorry, there was an error converting your file.\n'
                'The file might be corrupted or in an unsupported format.\n\n'
                'Please try again with a different file.'
            )
            return ConversationHandler.END

    except Exception as e:
        logging.error(f"Error in convert_file: {str(e)}")
        await update.message.reply_text(
            '❌ Sorry, something went wrong.\n'
            'Please try again or contact support if the problem persists.'
        )
        return ConversationHandler.END

    finally:
        # Cleanup temporary files
        try:
            if input_path and os.path.exists(input_path):
                os.remove(input_path)
            if output_path and os.path.exists(output_path):
                os.remove(output_path)
            if progress_message:
                try:
                    await progress_message.delete()
                except:
                    pass
        except Exception as e:
            logging.error(f"Error cleaning up files: {str(e)}")

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file)],
        states={
            FORMAT_SELECTION: [
                MessageHandler(
                    filters.Regex('^(📄 Convert to PDF 📱|📄 Convert to PDF 📊|🖼️ Convert to JPG 🎨|🖼️ Convert to PNG 🎨|📊 Convert to XLSX 📈|📊 Convert to CSV 📉|❌ Cancel ↩️|Convert another file 📤)$'),
                    convert_file
                )
            ],
        },
        fallbacks=[],
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
