from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

def roll_dice():
    """Simulates rolling a dice."""
    return random.randint(1, 6)

def challenge_buttons(challenger, challenged):
    """Returns inline buttons for confirming or canceling a challenge."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{challenger}_{challenged}"),
                InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{challenger}_{challenged}"),
            ]
        ]
    )

def play_round():
    """Plays one round of the dice game."""
    return roll_dice()
