"""
Helper script to get your Telegram chat_id.
Run this and send a message to your bot, then it will print your chat_id.
"""
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")
if not token:
    print("ERROR: TELEGRAM_TOKEN not found in .env file")
    exit(1)

bot = Bot(token=token)
print(f"Bot username: @{bot.get_me().username}")
print("\nNow send ANY message to your bot in Telegram...")
print("Waiting for messages...\n")

last_update_id = None
while True:
    updates = bot.get_updates(offset=last_update_id, timeout=10)
    for update in updates:
        if update.message:
            chat_id = update.message.chat.id
            username = update.message.chat.username or "N/A"
            first_name = update.message.chat.first_name or "N/A"
            print(f"✓ Message received!")
            print(f"  Chat ID: {chat_id}")
            print(f"  Username: @{username}")
            print(f"  Name: {first_name}")
            print(f"\nUse this Chat ID in your .env file:")
            print(f"TELEGRAM_CHAT_ID={chat_id}")
            exit(0)
        last_update_id = update.update_id + 1

