from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.buttons import start_buttons

async def start(client, message):
    text = (
        "🎲 **Welcome to Dice Game Bot!**\n\n"
        "Use the buttons below to explore and start playing.\n\n"
        "Tap **Help** for detailed game rules or **Commands** to see available commands."
    )
    await message.reply(text, reply_markup=start_buttons())

async def callback_handler(client, query: CallbackQuery):
    if query.data == "help":
        help_text = (
            "🎲 **Brief Rules of Dice Game**\n\n"
            "1️⃣ **Game Start**: Each player has 3 dice. Roll and hide them.\n"
            "2️⃣ **Bidding**: Players make bids on total dice values.\n"
            "3️⃣ **Challenge**: If challenged, dice are revealed to determine the winner.\n"
            "4️⃣ **Lose Dice**: Loser loses one die. Eliminate opponents to win!\n\n"
            "Use `/challenge @username` to start a challenge."
        )
        await query.message.edit(help_text, reply_markup=start_buttons())

    elif query.data == "commands":
        commands_text = (
            "🎮 **Available Commands**\n\n"
            "`/start` - Show welcome message and buttons\n"
            "`/help` - Detailed game rules\n"
            "`/challenge @username` - Challenge another player\n"
            "`/dice [amount]` - Roll dice with a bet\n"
            "`/leaderboard` - Show game leaderboard\n"
        )
        await query.message.edit(commands_text, reply_markup=start_buttons())
