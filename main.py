# Import libraries
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import cv2
import pytesseract
import os, re

# Base variables
DOWNLOAD_LOCATION = "./temp/"

# Send welcome message to new users
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to my youtube downloader bot.')


# Downlaod photo, OCR image and finally send text to user
def ocr_photo(update: Update, context: CallbackContext) -> None:
    file_id = update.message.photo[-1].file_id
    file = context.bot.getFile(file_id)
    file_path = f'./temp/{file_id}'
    file.download(file_path)
    text = ocr(file_path)
    os.remove(file_path)
    update.message.reply_text(text)


# Downlaod image that send as document, OCR image and finally send text to user
def ocr_document(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.getFile(file_id)
    file_path = f'./temp/{file_id}'
    file.download(file_path)
    text = ocr(file_path)
    os.remove(file_path)
    update.message.reply_text(text)

# Preprocess and OCR image and return it's text
def ocr(file_path):
    img_cv = cv2.imread(file_path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb, lang="fas")
    return text


if __name__ == '__main__':
    updater = Updater(token='TOKEN')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, ocr_photo))
    dispatcher.add_handler(MessageHandler(Filters.document.category('image'), ocr_document))
    updater.start_polling()
    updater.idle()
