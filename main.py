import discord
from discord.ext import commands
import re  # Import regular expressions module for URL detection
import asyncio
import os  # Import os module to access environment variables
from keep_alive import keep_alive  # Import keep_alive function

# Retrieve the bot token from environment variables
TOKEN = os.getenv('TOKEN')

# Replace with your channel ID
CHANNEL_ID = 1149611091098341437

# Regular expression pattern to detect URLs
url_pattern = re.compile(r'https?://\S+')

# Define the intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Enable reading message content

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Set bot's "about me" profile section
    about_me_text = "Programmed By: @u6y\n.gg/656"
    await bot.change_presence(activity=discord.Game(name=about_me_text))
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and not message.author.bot:
        # Check if the message contains a URL
        if url_pattern.search(message.content):
            # If URL found, send a warning message and delete the message
            await message.delete()
            warn_message = await message.channel.send(f"{message.author.mention}, please do not send messages containing links.")
            await asyncio.sleep(5)
            await warn_message.delete()
            return

        # Create the embed with the message content
        embed = discord.Embed(
            description=f'**{message.content}**',  # Include the message content in the embed
            color=discord.Color.from_rgb(240, 228, 216)  # Light blue color (RGB: 171, 219, 227)
        )
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
        embed.set_footer(text=f'UAE • {message.created_at.strftime("%Y-%m-%d %H:%M:%S")}')
        # Set thumbnail to the server's icon
        if message.guild.icon:
            embed.set_thumbnail(url=message.guild.icon.url)

        # Send the embed message
        sent_message = await message.channel.send(embed=embed)
        await sent_message.add_reaction('<a:00E:1190192673257164800>')
        await sent_message.add_reaction('<a:28:1190230116236795925>')
        await sent_message.add_reaction('<a:1540_PeePeeHands8:1130824705415319724>')

        # Delete the original message
        await message.delete()

        return  # Stop further processing of this message to prevent duplicate sends

# Run the bot
bot.run(TOKEN)

# Keep the Flask server alive
keep_alive()