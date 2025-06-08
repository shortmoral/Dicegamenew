from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.game_logic import challenge_buttons, play_round
# Dictionary to keep track of active challenges
active_challenges = {}

async def start(client: Client, message: Message):
    """Handles the /start command."""
    if message.chat.type == "private":
        await message.reply(
            "👋 Welcome to the Dice Game Bot!\n\n"
            "Use /help to see the available commands and get started."
        )
    else:
        await message.reply("👋 Hi! Use /help to see the commands.")

async def help_command(client: Client, message: Message):
    """Handles the /help command."""
    await message.reply(
        "🎲 **Dice Game Bot Commands**:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/challenge - Challenge another user to a dice game\n\n"
        "To challenge someone, reply to their message or mention their username with the /challenge command."
    )

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

    if action == "confirm":
        active_challenges[(challenger, challenged)]["state"] = "active"
        await query.message.edit(
            f"✅ Challenge confirmed! {query.from_user.mention} vs {(await client.get_users(challenger if query.from_user.id == challenged else challenged)).mention}.\nLet the game begin!"
        )
        await query.answer()

        # Roll dice for both users
        challenger_roll = play_round()
        challenged_roll = play_round()

        # Determine winner
        if challenger_roll > challenged_roll:
            winner = challenger
        elif challenged_roll > challenger_roll:
            winner = challenged
        else:
            winner = None

        # Reply with results
        results_message = (
            f"🎲 **Results**:\n"
            f"{(await client.get_users(challenger)).mention} rolled: {challenger_roll}\n"
            f"{(await client.get_users(challenged)).mention} rolled: {challenged_roll}\n\n"
        )
        if winner:
            results_message += f"🏆 **Winner**: {(await client.get_users(winner)).mention}"
        else:
            results_message += "🤝 **It's a draw!**"

        await query.message.reply(results_message)
        active_challenges.pop((challenger, challenged), None)

# Register Handlers
def register_handlers(app: Client):
    app.add_handler(filters.command("start"), start)
    app.add_handler(filters.command("help"), help_command)
    app.add_handler(filters.command("challenge"), challenge)
    app.add_handler(filters.callback_query, callback_handler)
