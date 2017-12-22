import meme_bot
import signal
import asyncio

bot = meme_bot.MemeBot()
# Ensure graceful exit
signal.signal(signal.SIGTERM, bot.shutdown)
signal.signal(signal.SIGINT, bot.shutdown)


@bot.command(pass_context=True)
async def subscribe(ctx):
    """Subscribes a user to this bot's user list"""
    user = ctx.message.author
    if user.id in bot.users:
        await bot.send_message(user, "You're already subscribed!")
    else:
        bot.users.append(user.id)
        await bot.send_message(user, "Thank you for subscribing to memebot!")


@bot.command(pass_context=True)
async def unsubscribe(ctx):
    """Unsubscribes a user from this bot's user list"""
    user = ctx.message.author
    if user.id in bot.users:
        bot.users.remove(user.id)
        await bot.send_message(user, "You have unsubscribed from memebot!")
    else:
        await bot.send_message(user, "You aren't subscribed to memebot in the"
                                  " first place!")


async def check_for_memes():
    await bot.wait_until_ready()
    while not bot.is_closed:
        await bot.send_meme()
        await asyncio.sleep(300)

bot.loop.create_task(check_for_memes())

# Get bot token and run
with open("token.txt", "r") as f:
    token = f.read()
bot.run(token)
