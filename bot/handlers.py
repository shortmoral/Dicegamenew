from pyrogram import Client, filters

async def challenge(client, message):
    text = (
        "⚔️ **Challenge Initiated!**\n\n"
        "Tag another player to start the challenge:\n"
        "`/challenge @username`"
    )
    await message.reply(text)
