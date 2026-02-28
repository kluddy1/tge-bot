import typing
import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import random
import time
import datetime

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
bump_streak_world_record = 9
current_bumper = ""
bump_channels = set()
last_executed_mention = time.time()
last_executed_jorblecock = time.time()
last_status_update = time.time()

bot = commands.Bot(command_prefix='/', intents=intents)

# Turning bot on

@bot.event
async def on_ready():
    print(f"hi i'm {bot.user.name} and i'm ready")
    log_channel = bot.get_channel(1420791229293265000)
    status_channel = bot.get_channel(1477362692728819947)
    await log_channel.send("yo gurt i am up and running")
    await status_channel.send("bot should be up and running")
    await status()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        await log_channel.send(f"{len(synced)} commands synced successfully vro")
    except Exception as e:
        print(e)

# Slash commands

@bot.tree.command(name="bump", description="bump the server to achieve nothing but bragging rights for the next 2 hours")
@app_commands.checks.cooldown(1,7200, key=lambda i: (i.channel_id))
async def bump(interaction: discord.Interaction):
    global current_bumper
    global bump_streak
    global bump_streak_world_record
    if interaction.channel.id == 1418641115409813686 or interaction.channel.id == 1309820906100490271:
        previous_bumper = current_bumper
        current_bumper = interaction.user.id

        if current_bumper == previous_bumper:
            bump_streak += 1
        else:
            bump_streak = 1

        if bump_streak > 1:
            if bump_streak > bump_streak_world_record:
                await interaction.response.send_message(f"Thanks for bumping, {interaction.user.mention}! They are currently on a streak of {bump_streak} bumps in a row , which is a new world record!!! This does nothing for the server, but you win!!! Congrats!!!!! You now get bragging rights for the next 2 hours, which is when I will remind you next.")
                bump_streak_world_record = bump_streak
            else:
                await interaction.response.send_message(
                    f"Thanks for bumping, {interaction.user.mention}! They are currently on a streak of {bump_streak} bumps in a row (yes i added words to avoid the accidental factorial)! This does nothing for the server, but you win!!! Congrats!!!!! You now get bragging rights for the next 2 hours, which is when I will remind you next.")
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
    bump_channels.add(interaction.channel.id)
    print(bump_channels)

@bot.tree.command(name="pet", description="pet emoji")
async def pet(interaction: discord.Interaction):
    await interaction.response.send_message(f"https://cdn.discordapp.com/attachments/1245987865943474269/1445129374218190929/TGEPET.gif?ex=692f391c&is=692de79c&hm=15b52d62b7eb08843e736ef47cfc5f22d1e573f13f0e14eeee4ba496b7b94703&")

@bot.tree.command(name="jorblecock", description="jorblecock your friends! 😃")
async def send_message_as_bot(interaction: discord.Interaction, who: typing.Optional[str]):
    global last_executed_jorblecock
    if time.time() > last_executed_jorblecock + 10:
        if who == "<@1418634609637458040>":
            await interaction.response.send_message(
                f"You cannot jorblecock me, <@{interaction.user.id}>.")
            last_executed_jorblecock = time.time()
            return
        if who:
            await interaction.response.send_message(f"{who}! You just got: Jorblecocked! 😂 repost to jorblecock your friends")
            last_executed_jorblecock = time.time()
        else:
            await interaction.response.send_message(
                f"<@{interaction.user.id}> just jorblecocked themselves because they didn't enter a person to jorblecock!")
            last_executed_jorblecock = time.time()
    else:
        await interaction.response.send_message("don't FUCKING spam please thanks", ephemeral=True)

# @bot.tree.command(name="impregnate", description="🫃")
# async def impregnate(itx, channel: discord.TextChannel, who: typing.Optional[str]):
#     global last_executed_impregnation
#     if time.time() > last_executed_impregnation + 0:
#         await itx.response.send_message(f"{who}! You just got: impregnated! 🫃 repost to imprgenanté your friends")
#         message_id = itx.id
#         msg = await channel.fetch_message(message_id)
#         msg.add_reaction("🫃")
#         last_executed_impregnation = time.time()
#     else:
#         await itx.response.send_message(
#             f"it has not been 9 months yet, still pregnant", ephemeral=True)

# !: ILLEGAL COMMANDS

@bot.tree.command()
async def ban(ctx, member : discord.Member, *, reason:typing.Optional[str]):
    if ctx.user.id == 776464268966625290:
        await member.ban(reason = reason)
    else:
        await ctx.response.send_message("You aren't kluddy.", ephemeral=True)

# @bot.tree.command(name="timeout", description="timeout your friends 😐")
# async def timeout(ctx: commands.Context, member: discord.Member):
#     if ctx.user.id == 776464268966625290:
#         await member.timeout(datetime.timedelta(seconds=60), reason=f"Requested by kluddy")
#         await ctx.response.send_message(f"I've timed out the guy for 1 minute.", ephemeral=True)
#     else:
#         await ctx.response.send_message("You aren't kluddy.", ephemeral=True)

# TODO: Add bump leaderboard

# Status

async def status():
    global last_status_update
    status_channel = bot.get_channel(1477362692728819947)
    last_status_update = time.time()
    await status_channel.send(f"bot running <t:{int(last_status_update)}:R>. If this is over 5 minutes ago, the bot is down.")
    await asyncio.sleep(300)

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

# Reference handler, deprecated

# @bot.event
# async def on_message2(message):
#     print("message detected")
#     if message.author.id == 744122961509744660:
#         number = random.randint(1,1000)
#         if number == 777:
#             await message.channel.send("DUCKS oooo scary hahaha DUUUCKS DUUUUUUUUCKS BE SCARED DAVER BOY")
#
#     elif message.author.id == 776464268966625290:
#         print("hi 1")
#         number = random.randint(1, 2)
#         print(number)
#         if number == 1:
#             await message.channel.send("hi father")
#             print("hi")

# reference handler real

@bot.event
async def on_message(message):
    global last_executed_mention
    random_line_list = [
        "hi",
        "ok",
        f"<@{message.author.id}>, stay determined!",
        "we don't like 7 days to die around these parts",
        "literally 1984 smh",
        "uh umm uhh uhhh umm uh",
        "this is the 7th item in this list, isn't that absolutely bonkers",
        "how many days?",
        "7 what?",
        "7 days",
        "this is one hell of a daver the dave moment :joy_cat:",
        "this cat just j",
        "hi i'm james",
        "shameless kluddy plug: <https://youtube.com/@kluddy>",
        "visit the 7 days subreddit at <https://www.reddit.com/r/7DaysOfficial/>!!!!",
        "WOAH",
        ":wob:",
        ":truege:",
        "KEEP DAYING!!!",
        "the guy ever never ever lever dever sever bever",
        "S",
        "h",
        "dude why is the letter j so funny though",
        "https://tenor.com/view/skull-epic-cool-cool-skeleton-keyboard-gif-9406471634714037785",
        "go buy 7 days at https://store.steampowered.com/app/3247640/7_Days/",
        "this is your free ticket to ping kluddy once",
        "hi saf",
        "|| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| ||",
        "ibr i ain't reading allat",
        "https://tenor.com/view/icindustries-7days-7-days-ic-industries-7-days-for-free-gif-4480538362982609995",
        "ARE YOU READY TO FACE YOUR TRAUMAS IN 7 DAYS, THE ULTIMATE RPG MAKER GAME! WALK AROUND IN A DREAMLIKE WORLD, TALK TO PEOPLE AND PUT ON YOUR SHEET TO LOOK AT YOUR PAST! FIGHT YOUR INNER DEMONS! THERE'S NO COMBAT BUT WHO CARES! EAT BREAKFAST! VISIT THE CAT CITY! WITH CATS! MINIGAMES! PUZZLES! SAWDUST BREAD! WITNESS EMOTIONAL FLASHBACKS THAT WILL RIP YOUR HEART OUT AND THROW IT INTO A BLENDER! 7 DAYS: FACE YOURSELF! Available August 29th on Steam.",
        "7",
        "days",
        "MIKAEEEEEEEEEEEEEEL!!!!!!!!!!! DONT LEAVE ME HERE MIKAELLLL!!!!!",
        f"`There’s a block in front of you.`\n`You start pushing onwards.`\n`For what feels like an eternity.`\n`Eyes stare at you in your absurd task.`\n`Yet duty calls, there’s no time to think about that.`",
        "apple",
        "Stanley looked around as his mind couldn't comprehend the limits of his current space",
        "yeah!",
        "no",
        "fuck nightbot",
        "gays",
        "nightbot",
        "man i wish i could go become a worker at a family bakery or something instead of being some clanker working for a discord server",
        "portal 2 is the best game ever",
        "In mathematics, the Riemann hypothesis is the conjecture that the Riemann zeta function has its zeros only at the negative even integers and complex numbers with real part ⁠1/2⁠. Many consider it to be the most important unsolved problem in pure mathematics. It is of great interest in number theory because it implies results about the distribution of prime numbers. It was proposed by Bernhard Riemann (1859), after whom it is named. ",
        "sunny is my number 1 hater and i don't know why, it doesn't even matter how hard i try, keep that in mind i designed this rhyme to explain in due time",
        f"I am john.\nThis is truly a 7 days.",
        f"greetch jorblecock is not just a song it is a lifestyle event a personal awakening and possibly a small goblin screaming inside your soul and that is beautiful. the first time i heard greetch jorblecock i did not understand it but that is the point because understanding is for cowards and this song is brave. it slaps you gently and then steals your lunch money while whispering wisdom that sounds like nonsense. the noises do not follow rules and honestly rules have had it too good for too long. the melody crawls instead of walks and that makes it more honest. when the beat does something weird and uncomfortable it feels like the song is looking directly at you and saying yeah i know and i dont care. that confidence alone deserves praise and possibly a small parade.\n the lyrics of greetch jorblecock feel like they were written on a napkin during a moment of divine confusion and that is peak art. every line feels like it tripped down the stairs but landed perfectly. it makes you feel smart and stupid at the same time which is rare and powerful. when i listen to it i feel like a creature just crawled out of a swamp and handed me emotional truth wrapped in slime. the song does not try to be deep but accidentally is and that is way better than trying. greetch jorblecock plays and suddenly the world makes less sense but in a good way like when you spin around until you fall over and laugh at the ceiling. this song should be studied yelled played too loud at night and defended aggressively. greetch jorblecock is chaos joy noise and heart all mashed together and i respect it more than most things including silence.",
        "<@1418634609637458040>",
        "saif is probably bored",
        f"`I've seen enough` \n- blind person",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1420832717351944233/ABSOLUTE0001.png?ex=68d6d515&is=68d58395&hm=6626e2ea377eb1850740a672b94f9293e96b26e95a8ffd8486e7a8b0371e1002&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1420832633260085398/tumblr_22d695bcdc4fe53906c10f8741b2b403_16c83577_2048.jpg?ex=68d6d501&is=68d58381&hm=080e4224f08d2ccd34ad0321bf9ae5f5f55a889532fe440a44161673147d09ee&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1420830985443872921/ITS_NOT_OVER.png?ex=68d6d378&is=68d581f8&hm=a9cf7b98dcbc30f7e1e89ae7ca8533a13eab1f5071852ac760ed65034bf095be&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1420830953739260046/image.png?ex=68d6d371&is=68d581f1&hm=c57eb9cb86c195d0c7036becb6a50ec641813b3f52492f096ccf95916b628a3b&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1420830483352129606/SOMETHING_WILL_HAPPEN.png?ex=68d6d300&is=68d58180&hm=5c17bee7609dca29443ce61b7a974648995a2bd942c1d6bb14e31f1550001494&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1420833290952249404/DYNAMITE1.png?ex=68d6d59e&is=68d5841e&hm=6a6c560f7c5ae67faa9050e77c40263fab263f6bef6c4fa4bad4913b5549acb5&",
        "https://cdn.discordapp.com/attachments/1419096307972440187/1421158240804278324/WWWUUAAAGGH.mp4?ex=68d80440&is=68d6b2c0&hm=94fea1cee2a52b8c2cce6a5784d878e8023161a1e9febdde3c21fdd195319244&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1422637030130847834/attachment-1.gif?ex=68e3543b&is=68e202bb&hm=851c51e2488cdb6be2926ce2109ec2345e0c6d53b3a071187043f7d375db0676&",
        "https://cdn.discordapp.com/attachments/1245987865943474269/1425935027979554967/ScreenRecording_09-25-2025_6-06-19_pm_1.mov?ex=68e964fb&is=68e8137b&hm=0c207cbbd8358ffd7b248bb3a37d922310874b805b1a9fc06e7f9716ad3c2c84&",
        "https://cdn.discordapp.com/attachments/1374843296819445883/1432144443145846834/makesweet-j8uiur.gif?ex=6911c833&is=691076b3&hm=f062e560125aceabf592968ea3c33d7766c042c14fbe95c1a1318279e5803e78&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1422888900010967122/IMG-20250930-WA0012.jpg?ex=69a4110d&is=69a2bf8d&hm=b45c0d23c1cd82cf0088dc820b285611e7798ce9228a1805a55656b9b818ddd8&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1423928613425643620/ABSOLUTE_trench_face.png?ex=69a3e4dc&is=69a2935c&hm=d86152a73632aeebcd2e5187fa370c169b8bc99a8c0afb1a1fdf00301ff07033&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1462531578084200651/A7DAYS.gif?ex=69a3ecec&is=69a29b6c&hm=364ec231a23a44ccf81bcc61a25271e2b74c7e6749942991f093976321c41977&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1462531752055542033/YIPWAAAAAA.mp4?ex=69a3ed16&is=69a29b96&hm=b29bbc6145150887542c0fd4d5ad4a2ec3022035e5c12af45d68ab202cf074f2&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1465998784864452731/SPOILER_image-3.png?ex=69a403c3&is=69a2b243&hm=d3a7e6562389a7627f4eb637a7e4c2a16585ea3727d100542e36e08b4ddc8310&",
        "https://cdn.discordapp.com/attachments/1420819821318115418/1465998786089324544/RDT_20260126_0129104579757757918538628.jpg?ex=69a403c3&is=69a2b243&hm=60155723af92f7380d991f6406248181dda71a728e873ed568306a5cfab39549&",
        "https://tenor.com/view/demokinght-demo-tf2-skeleton-bash-shield-gif-2966363169766827880"

    ]

    if message.author.id == 83010416610906112 and "hi" in message.content.lower():
        await message.channel.send("shut up nightbot no one likes you")

    if message.author == bot.user:
        return

    if message.author.id == 1012306381233197086:
        if random.randint(0,999) == 696:
            await message.channel.send("ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ")

    if "<@1418634609637458040>" in message.content:
        if last_executed_mention + 5.0 < time.time() or message.author.id == 776464268966625290:
            last_executed_mention = time.time()
            if any(s in message.content.lower() for s in ("gn", "goodnight", "good night")):
                await message.channel.send(f"good night, <@{message.author.id}>!")
                await message.channel.send(f"https://media.discordapp.net/attachments/1245987865943474269/1466174861394055371/image.png?ex=697bc93f&is=697a77bf&hm=c981f514be64ed6e978b973eaed0762fec4c67aa04423b5e091c0ee3e3c2332c&animated=true")
            elif any(s in message.content.lower() for s in ("gm", "goodmorning", "good morning")):
                await message.channel.send(f"good morning, <@{message.author.id}>!")
            elif "fuck you" in message.content.lower():
                await message.channel.send("fuck you too")
            else:
                await message.channel.send(random_line_list[random.randint(0, len(random_line_list) - 1)])
        else:
            print(f"{message.author.id} is tryna spam ping the bot!!!")

    if "totr" in message.content.lower():
        await message.channel.send("SHUT THE FUCK UP ABOUT TOTR")

    if "hell yeah" in message.content.lower():
        await message.channel.send("https://cdn.discordapp.com/attachments/1236429241181143179/1337031531813666826/hellyeah.gif?ex=68d681a6&is=68d53026&hm=5ffd65a3ebd2d4bb68d0eb1c4d32fe7baa10ded1c0bdff56027b0744734cb1eb&")

    if "7" in message.content[0]:
        if "days" in message.content.lower():
            await message.channel.send("7 DAYS MENTIONED 🗣️🔥 RAAAHH WHAT THE FUCK IS A OMORI COPY⁉️ ⁉️ 🗣️ FUCK TRAUMAS 💪 🙏 ‼️ and also did you just say days? 😱 Like the... 7 Days? 🤔 Chat, is this a 7 Days reference? 😯 Chat! This is a 7 Days reference! 😂 BOI 🫱 you have won the internet today! 😁 Only the guys ever will understand")
        else:
            await message.channel.send("7 DAYS MENTIONED 🗣️🔥 RAAAHH WHAT THE FUCK IS A OMORI COPY⁉️ ⁉️ 🗣️ FUCK TRAUMAS 💪 🙏 ‼️")
    elif "days" in message.content.lower():
        await message.channel.send("Did you just say days? 😱 Like the... 7 Days? 🤔 Chat, is this a 7 Days reference? 😯 Chat! This is a 7 Days reference! 😂 BOI 🫱 you have won the internet today! 😁 Only the guys ever will understand")

    if any(s in message.content.lower() for s in ("calc ", "calc?", "calc!", "calc")) and "calculator" not in message.content.lower():
        await message.channel.send("(stands for calculator)")
    elif "does calc stand for calculator?" in message.content.lower():
        await message.channel.send("yeah it does")

    if random.randint(0,999) == 67:
        await message.channel.send("vilu is awesome")

    await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)