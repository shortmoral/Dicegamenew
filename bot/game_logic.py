from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

def roll_dice():
    """
    Simulates rolling a dice.
    Returns:
        int: A random number between 1 and 6 inclusive.
    """
    return random.randint(1, 6)

def challenge_buttons(challenger, challenged):
    """
    Returns inline buttons for confirming or canceling a challenge.
    
    Args:
        challenger (int): User ID of the challenger.
        challenged (int): User ID of the challenged user.
    
    Returns:
        InlineKeyboardMarkup: Inline keyboard with confirm and cancel buttons.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Confirm", callback_data=f"confirm_{challenger}_{challenged}"
                ),
                InlineKeyboardButton(
                    "❌ Cancel", callback_data=f"cancel_{challenger}_{challenged}"
                ),
            ]
        ]
    )

def play_round():
    """
    Plays one round of the dice game by rolling a dice.
    
    Returns:
        int: The result of the dice roll for this round.
    """
    return roll_dice()
