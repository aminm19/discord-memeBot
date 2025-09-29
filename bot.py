import requests
import json
import discord
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def get_meme():
    response = requests.get("https://meme-api.com/gimme")
    json_data = json.loads(response.text)
    return json_data['url']

WELCOME_TEXT = (
    "Send '$meme' in the chat to test out the memeBot! I will send you a random meme from the internet. Have fun!"
)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$meme'):
            await message.channel.send(get_meme())

    async def on_member_join(self, member):
        """
        Send a welcome message in a server channel when a new member joins.
        Uses the guild's system channel if one is set; otherwise falls back to
        the first text channel the bot has permission to send messages in.
        """
        # Try the system channel first
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            for c in member.guild.text_channels:
                if c.permissions_for(member.guild.me).send_messages:
                    channel = c
                    break

        if channel is not None:
            # Mention the new member so they get notified
            await channel.send(f"Welcome {member.mention}! {WELCOME_TEXT}")
        else:
            # No channel found where the bot can send messages
            print(f"Could not find a channel to send welcome message in {member.guild.name}")

intents=discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for on_member_join
WELCOME_CHANNEL_ID=1394710844658417736

client = MyClient(intents = intents)
client.run(DISCORD_TOKEN)