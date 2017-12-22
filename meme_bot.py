import praw
import discord
from discord.ext import commands
import os


class MemeBot(commands.Bot):
    """
    A bot which scrapes the 5 'hottest' memes from r/dankmemes and
    periodically sends them to a specified user
    """

    def __init__(self):
        """
        Initialize a new meme bot with a preset list of users and list of memes
        to ignore.
        """
        commands.Bot.__init__(self, description="Memes", command_prefix="!")
        self._reddit = praw.Reddit("meme_bot")

        # Initialize or load the list of subscribed users
        if not os.path.isfile("users.txt"):
            self.users = []
        else:
            with open("users.txt", "r") as f:
                users = f.read()
                self.users = users.split("\n")
                self.users = list(filter(None, self.users)) # Filter nulls

        # Initialize or load in a list of posts to ignore
        if not os.path.isfile('ignore.txt'):
            self.ignore = []
        else:
            with open("ignore.txt", "r") as f:
                posts = f.read()
                self.ignore = posts.split("\n")

    async def send_meme(self):
        """Sends a meme to every single user in the bot's list"""
        for submission in self._reddit.subreddit("dankmemes").hot(limit=10):
            if submission.id in self.ignore or submission.stickied:
                continue
            else:
                await self._send_meme_helper(submission)
                break

    async def _send_meme_helper(self, meme):
        # Ignore this meme from now on
        self.ignore.append(meme.id)

        # Create a discord embed to contain the meme
        embed = discord.Embed(title=meme.title,
                              type="rich",
                              color=0xAA00FF)
        embed.set_image(url=meme.url)
        embed.set_footer(text="Memes fresh from /r/dankmemes!")

        # Send meme to every subscribed user
        for user_id in self.users:
            user = await self.get_user_info(user_id)
            await self.send_message(user, embed=embed)

    def shutdown(self, signal, frame):
        """
        A signal handler that tells the bot to save its data before
        the program is terminated.
        """
        print("\nSaving bot status...")
        self._save()
        print("Saved.")
        exit(0)

    def _save(self):
        """Save users and ignore list to the file system"""
        with open("users.txt", "w") as f:
            for user in self.users:
                f.write("{}\n".format(user))
        with open("ignore.txt", "w") as f:
            for post in self.ignore:
                f.write("{}\n".format(post))



