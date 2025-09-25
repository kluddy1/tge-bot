import typing
import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Variables for various commands
bump_streak = 1
current_bumper = ""
bump_channels = []

bot = commands.Bot(command_prefix='/', intents=intents)

# Turning bot on

@bot.event
async def on_ready():
    print(f"hi i'm {bot.user.name} and i'm ready")
    log_channel = bot.get_channel(1420791229293265000)
    await log_channel.send("yo gurt i am up and running")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        await log_channel.send(f"{len(synced)} commands synced successfully vro")
    except Exception as e:
        print(e)

# Slash commands

@bot.tree.command(name="bump", description="bump the server to achieve nothing but bragging rights for the next 2 hours")
@app_commands.checks.cooldown(1,7200,key=lambda i: (i.guild_id))
async def bump(interaction: discord.Interaction):
    global current_bumper
    global bump_streak
    if interaction.channel.id in bump_channels:
        previous_bumper = current_bumper
        current_bumper = interaction.user.id

        if current_bumper == previous_bumper:
            bump_streak += 1
        else:
            bump_streak = 1

        if bump_streak > 1:
            await interaction.response.send_message(f"Thanks for bumping, {interaction.user.mention}! They are currently on a streak of {bump_streak}! This does nothing for the server, but you win!!! Congrats!!!!! You now get bragging rights for the next 2 hours, which is when I will remind you next.")
        else:
            await interaction.response.send_message(f"Thanks for bumping, {interaction.user.mention}! This does nothing for the server, but you win!!! Congrats!!!!! You now get bragging rights for the next 2 hours, which is when I will remind you next.")
        await asyncio.sleep(7200)
        await interaction.channel.send(f"<@&1310237621892419594> IT'S THAT TIME TO BUMP AGAIN GUYS YOO")
    else:
        await interaction.response.send_message("this is not the bump channel, go there to bump OR set this as the bump channel using /set_bump_channel if you are an administrator", ephemeral=True)

@bot.tree.command(name="send_message_as_bot", description="hi")
async def send_message_as_bot(interaction: discord.Interaction, arg: typing.Optional[str]):
    if interaction.user.id == 776464268966625290:
        await interaction.channel.send(f"{arg}")
    else:
        await interaction.response.send_message("You aren't kluddy.", ephemeral=True)

@bot.tree.command(name="set_bump_channel", description="set this channel to the bump channel automagically (kluddy does it manually)")
@app_commands.checks.has_permissions(administrator=True)
async def set_bump_channel(interaction: discord.Interaction):
    global bump_channels
    await interaction.channel.send(f"this command does NOT yet work correctly, and absolutely NOTHING has been changed\n-# <@776464268966625290> go change their bump channel manually stupid")
    bump_channels.append(interaction.channel.id)

# TODO: Add bump leaderboard

# Error handler

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    print("bro got an error")
    if isinstance(error, app_commands.CommandOnCooldown):
        print("it IS a cooldown error!")
        await interaction.response.send_message("This command is on cooldown, so STOP IT AND WAIT UNTIL I REMIND YOU", ephemeral = True)
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(f"You are NOT powerful enough, you are missing the {error.missing_permissions} permission(s)", ephemeral=True)
    else: raise error

# Reference handler

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.id == 83010416610906112:
        return

    if "totr" in message.content.lower():
        print("totr is the bane of my existence")
        await message.channel.send("SHUT THE FUCK UP ABOUT TOTR")

    if "days" in message.content.lower():
        await message.channel.send("Did you just say days? 😱 Like the... 7 Days? 🤔 Chat, is this a 7 Days reference? 😯 Chat! This is a 7 Days reference! 😂 BOI 🫱 you have won the internet today! 😁 Only the guys ever will understand")
        print("days but not 7")

    if "hell yeah" in message.content.lower():
        await message.channel.send("https://cdn.discordapp.com/attachments/1236429241181143179/1337031531813666826/hellyeah.gif?ex=68d681a6&is=68d53026&hm=5ffd65a3ebd2d4bb68d0eb1c4d32fe7baa10ded1c0bdff56027b0744734cb1eb&")

    await bot.process_commands(message)
"""
    if "7" in message.content.lower():
        print("7 present!!!!")
        if "days" in message.content.lower():
            await message.channel.send("7 DAYS MENTIONED 🗣️🔥 RAAAHH WHAT THE FUCK IS A OMORI COPY⁉️ ⁉️ 🗣️ FUCK TRAUMAS 💪 🙏 ‼️ and also did you just say days? 😱 Like the... 7 Days? 🤔 Chat, is this a 7 Days reference? 😯 Chat! This is a 7 Days reference! 😂 BOI 🫱 you have won the internet today! 😁 Only the guys ever will understand")
            print("Days present!!!!!")
        else:
            await message.channel.send("7 DAYS MENTIONED 🗣️🔥 RAAAHH WHAT THE FUCK IS A OMORI COPY⁉️ ⁉️ 🗣️ FUCK TRAUMAS 💪 🙏 ‼️")
            print("me when 7 but no days :pensive:")         
"""
    


bot.run(token, log_handler=handler, log_level=logging.DEBUG)

