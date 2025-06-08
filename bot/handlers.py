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

    if action == "confirm":
        if query.from_user.id != challenged:
            await query.answer("Only the challenged user can confirm!", show_alert=True)
            return

        active_challenges[(challenger, challenged)]["state"] = "playing"
        await query.message.edit(
            f"🎲 Challenge accepted! Let the game begin!\n\n"
            f"**{(await client.get_users(challenger)).mention} vs {query.from_user.mention}**"
        )
        await start_game(client, challenger, challenged, query.message.chat.id)

async def start_game(client: Client, challenger: int, challenged: int, chat_id: int):
    """Runs the game between two players."""
    results = {"challenger": 0, "challenged": 0}
    for round_num in range(1, 4):
        challenger_roll = play_round()
        challenged_roll = play_round()

        winner = (
            "challenger" if challenger_roll > challenged_roll else "challenged"
            if challenger_roll < challenged_roll
            else None
        )

        if winner:
            results[winner] += 1

        await client.send_message(
            chat_id,
            f"🎲 **Round {round_num} Results**:\n"
            f"{(await client.get_users(challenger)).mention} rolled: 🎲 {challenger_roll}\n"
            f"{(await client.get_users(challenged)).mention} rolled: 🎲 {challenged_roll}\n\n"
            f"**Winner**: {client.get_users(challenger).mention if winner == 'challenger' else client.get_users(challenged).mention if winner == 'challenged' else 'Draw!'}"
        )

    final_winner = (
        challenger if results["challenger"] > results["challenged"] else challenged
        if results["challenger"] < results["challenged"]
        else None
    )

    await client.send_message(
        chat_id,
        f"🏆 **Final Results**\n\n"
        f"{(await client.get_users(challenger)).mention}: {results['challenger']} wins\n"
        f"{(await client.get_users(challenged)).mention}: {results['challenged']} wins\n\n"
        f"**Winner**: {(await client.get_users(final_winner)).mention if final_winner else 'It\'s a Draw!'}"
    )
    active_challenges.pop((challenger, challenged), None)
