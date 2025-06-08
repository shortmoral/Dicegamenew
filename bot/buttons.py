
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Add Bot to Your Group", url="https://t.me/Dice_inchatbot?startgroup=true"),
                InlineKeyboardButton("💬 Support Chat", url="https://t.me/NazkiSupport"),
            ],
            [
                InlineKeyboardButton("👤 Owner Account", url="https://t.me/Sexologisted"),
                InlineKeyboardButton("📜 Help", callback_data="help"),
            ],
            [
                InlineKeyboardButton("🎮 Commands", callback_data="commands"),
            ],
        ]
    )
