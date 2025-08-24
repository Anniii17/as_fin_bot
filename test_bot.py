from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# ✅ Tumhara Bot Token
TOKEN = os.getenv("BOT_TOKEN")

# ----- Local images folder -----
IMAGE_FOLDER = os.path.join(os.getcwd())  # Script folder
AD_IMAGES = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg"]  # All 5 ad images

# ----- Function to build Options Keyboard -----
def get_options_keyboard():
    keyboard = [
        [InlineKeyboardButton("Used Car Loan", callback_data='used_car_loan')],
        [InlineKeyboardButton("Car Insurance", callback_data='car_insurance')],
        [InlineKeyboardButton("Two Wheeler Insurance", callback_data='two_wheeler_insurance')],
        [InlineKeyboardButton("Health Insurance", callback_data='health_insurance')],
        [InlineKeyboardButton("Home Loan", callback_data='home_loan')],
        [InlineKeyboardButton("Personal Loan", callback_data='personal_loan')],
        [InlineKeyboardButton("Contact Us", callback_data='contact')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ----- Start/Hello Handler -----
async def start_with_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ad_text = "💰 Apni car par 200% tak ka loan paye... Car bhi apki, paisa bhi apka! 🚗"

    # Send all ad images once
    for img_name in AD_IMAGES:
        img_path = os.path.join(IMAGE_FOLDER, img_name)
        if os.path.exists(img_path):
            with open(img_path, "rb") as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=ad_text)
    
    # Send service options
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your interest below:", reply_markup=get_options_keyboard())

# ----- Button Callback -----
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    service_data = {
        'used_car_loan': "🚗 Used Car Loan:\n- Up to 200% loan on your car.\n- Fast approval 1-3 days.",
        'car_insurance': "🚘 Car Insurance:\n- Comprehensive coverage.\n- Easy claims process.",
        'two_wheeler_insurance': "🏍️ Two Wheeler Insurance:\n- Protect your bike against accidents & theft.",
        'health_insurance': "💊 Health Insurance:\n- Coverage for you & family.\n- Cashless hospitalization.",
        'home_loan': "🏠 Home Loan:\n- Low interest rates & flexible repayment options.",
        'personal_loan': "💰 Personal Loan:\n- Fast approval, minimal documents.\n- Ideal for emergencies.",
    }

    if query.data in service_data:
        await query.edit_message_text(text=service_data[query.data])
        # Send only options again (without images)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose more options:", reply_markup=get_options_keyboard())
    elif query.data == 'contact':
        contact_text = (
            "📞 Contact Us:\n"
            "Phone: +91-9250287853\n"
            "Email: asfinancialservices65@gmail.com\n"
            "Website: as-financial-services.netlify.app"
        )
        await query.edit_message_text(text=contact_text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose more options:", reply_markup=get_options_keyboard())

# ----- Handle Text -----
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(word in text for word in ["hi", "hello", "start"]):
        await start_with_images(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Type 'hi' or 'hello' to see options again.")

# ----- Build App -----
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start_with_images))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(CallbackQueryHandler(button_callback))

print("AS Financial Services Bot is running... ✅")
app.run_polling()
