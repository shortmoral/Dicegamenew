from pyrogram import Client
from bot.handlers import challenge, callback_handler
from pyrogram import filters
from config import API_ID, API_HASH, BOT_TOKEN
app = Client("dice_game_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("challenge"))
async def challenge_command(client, message):
    await challenge(client, message)

@app.on_callback_query()
async def callback_query_handler(client, query):
    await callback_handler(client, query)

if __name__ == "__main__":
    print("🚀 Bot is running...")
    app.run()
