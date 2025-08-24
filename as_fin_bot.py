print("Bot script started... ✅")
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# ✅ Bot token


TOKEN = "TOKEN = 8377300382:AAFDuUyBlmxe_fUJBTEOdA7-s2ceWfPMri8"

# ----- Local images folder -----
IMAGE_FOLDER = os.path.join(os.getcwd())  # Images folder is same as script folder
AD_IMAGES = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg"]  # All 5 ad images

# ----- Function to send images once -----
async def send_images_once(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ad_text = "💰 Apni car par 200% tak ka loan paye... Car bhi apki, paisa bhi apka! 🚗"
    for img_name in AD_IMAGES:
        img_path = os.path.join(IMAGE_FOLDER, img_name)
        if os.path.exists(img_path):
            with open(img_path, "rb") as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=ad_text)
        else:
            print(f"Image not found: {img_path}")

# ----- Function to send only buttons -----
async def send_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Used Car Loan", callback_data='used_car_loan')],
        [InlineKeyboardButton("Car Insurance", callback_data='car_insurance')],
        [InlineKeyboardButton("Two Wheeler Insurance", callback_data='two_wheeler_insurance')],
        [InlineKeyboardButton("Health Insurance", callback_data='health_insurance')],
        [InlineKeyboardButton("Home Loan", callback_data='home_loan')],
        [InlineKeyboardButton("Personal Loan", callback_data='personal_loan')],
        [InlineKeyboardButton("Contact Us", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your interest below:", reply_markup=reply_markup)

# ----- Start / Greeting Function -----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_images_once(update, context)   # Images sent only once
    await send_buttons(update, context)       # Buttons

# --
