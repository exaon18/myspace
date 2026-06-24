import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging so you can see what's happening
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# 1. Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # A cozy welcome message matching your app's theme
    welcome_text = (
        "✨ Welcome to My Space ✨\n\n"
        "Pull up a chair, get comfortable, and chill by the fire. "
        "Tap the button below to step into your space."
    )
    
    # ⚠️ REPLACE THIS with your actual deployed Mini App URL
    MINI_APP_URL = "https://czfj013d-8000.euw.devtunnels.ms/" 
    
    # 2. Create the inline keyboard button with WebAppInfo
    keyboard = [
        [
            InlineKeyboardButton(
                text="⛺ Enter My Space", 
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 3. Send the message with the button attached
    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup)

def main():
    # ⚠️ REPLACE THIS with your Bot Token from @BotFather
    BOT_TOKEN = "8931595168:AAHSAaKz6ld4OKtb-fkS2C-raUlyevQ_zt8"
    
    # Build the Telegram application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the /start command
    application.add_handler(CommandHandler("start", start))

    # Run the bot
    print("Bot is running... Time to relax. ☕")
    application.run_polling()

if __name__ == "__main__":
    main()