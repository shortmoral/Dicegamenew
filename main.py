from pyrogram import Client
from bot.handlers import challenge, callback_handler
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the bot client
app = Client(
    "dice_game_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Import and register the handlers from start.py and game logic
from bot.start import start_command, help_command

app.add_handler(start_command)
app.add_handler(help_command)

@app.on_message(filters.command("challenge"))
async def challenge_command(client, message):
    await challenge(client, message)

@app.on_callback_query()
async def callback_query_handler(client, query):
    await callback_handler(client, query)

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
