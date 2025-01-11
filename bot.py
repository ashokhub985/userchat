from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Replace with your bot's token and admin chat ID using environment variables
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Function to handle new messages
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    username = user.username if user.username else "No username"
    first_name = user.first_name
    last_name = user.last_name if user.last_name else "No last name"

    message_text = f"New Message from: {first_name} {last_name}\nUsername: @{username}\nUser ID: {user_id}\nMessage: {update.message.text}"

    # Forward the message details to the admin
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message_text)

    # Reply to user
    update.message.reply_text(f"Hello {first_name}, your message has been received!")

# Function to reply to user from admin
def reply_to_user(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == int(ADMIN_CHAT_ID):  # Check if the message is from admin
        # Admin sends a message to a user
        message = " ".join(context.args)
        user_id = int(context.args[0])  # User ID as first argument
        context.bot.send_message(chat_id=user_id, text=message)

# Main function to run the bot
def main():
    updater = Updater(TOKEN)

    # Register handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, start))
    updater.dispatcher.add_handler(CommandHandler("reply", reply_to_user))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
