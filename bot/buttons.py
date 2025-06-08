
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Add Bot to Your Group", url="https://t.me/YourBotUsername?startgroup=true"),
                InlineKeyboardButton("💬 Support Chat", url="https://t.me/SupportChat"),
            ],
            [
                InlineKeyboardButton("👤 Owner Account", url="https://t.me/OwnerUsername"),
                InlineKeyboardButton("📜 Help", callback_data="help"),
            ],
            [
                InlineKeyboardButton("🎮 Commands", callback_data="commands"),
            ],
        ]
    )
