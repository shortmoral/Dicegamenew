from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from bot.game_logic import challenge_buttons, play_round

# Dictionary to keep track of active challenges
active_challenges = {}

async def challenge(client: Client, message: Message):
    """Handles the /challenge command."""
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply("⚠️ Reply to a user's message or mention a username to challenge them!")
        return

    challenger = message.from_user.id
    challenged = (
        message.reply_to_message.from_user.id if message.reply_to_message else (await client.get_users(message.command[1])).id
    )

    if challenger == challenged:
        await message.reply("⚠️ You can't challenge yourself!")
        return

    active_challenges[(challenger, challenged)] = {"rounds": [], "state": "pending"}
    await message.reply(
        f"⚔️ {message.from_user.mention} has challenged {(await client.get_users(challenged)).mention}!",
        reply_markup=challenge_buttons(challenger, challenged),
    )

async def callback_handler(client: Client, query: CallbackQuery):
    """Handles challenge inline button actions."""
    data = query.data.split("_")
    action, challenger, challenged = data[0], int(data[1]), int(data[2])

    if query.from_user.id not in [challenger, challenged]:
        await query.answer("This button is not for you!", show_alert=True)
        return

    if action == "cancel":
        if query.from_user.id != challenged:
            await query.answer("Only the challenged user can cancel!", show_alert=True)
            return

        active_challenges.pop((challenger, challenged), None)
        await query.message.edit(f"❌ Challenge canceled by {query.from_user.mention}.")
        return
