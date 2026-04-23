import nextcord
from nextcord.ext import commands
import base64
from easy_pil import *
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from os import getenv

dotenv_path = r"resources\secrets.env" # replace with path to .env file containing token
load_dotenv(dotenv_path=dotenv_path)
TOKEN = getenv('TOKEN')

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
intents.voice_states = True

bot = commands.Bot(intents=intents, command_prefix='fp$')
ownID = [373266820792188928, 1178550088436563973, 1226410848533217310,1217689235268702232]
permitted_promo = []

CREATOR_UPDATES_ROLE_ID = 1484378677365178429
CREATOR_UPDATES_CHANNEL_ID = 1484378170156257402
FINGER_PAINTER_ROLE_ID = 1483258332952137758
ILLUSTRATOR_ROLE_ID = 1484391404343132210
WELCOME_CHANNEL_ID = 1484390149830869042
ADMIN_CHANNEL_ID = 1483281945440813117
COMMUNITY_ROLE_ID = 1483261055474995362
PROMOTION_FORUM_ID = 1486382662708101222
bannable_words = [base64.b64decode(i).decode('utf-8') for i in ["bmlja2E=", "bmlja2Vy", "bmlnYQ==", "bmlnZ2E=", "bmlnZ2Vy", "ZmFnZ290", "ZmFn", "bmdh"]]
swear_words = ["fuck","bitch","shit","cunt","dick","pussy","tit","whore"]

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    guilds = list(bot.guilds)
    server_count = len(guilds)
    gnamelist = []
    for guild in guilds:
        guilds = list(bot.guilds)
    server_count = len(guilds)
    gnamelist = []
    gentry = []
    gentry.append(guild.name)
    gentry.append(guild.member_count)
    gnamelist.append(gentry)
    gnamelist.sort(key=lambda guild: guild[1], reverse=True)
    for guild in gnamelist:
        print(f"Name: {guild[0]}, Members: {guild[1]}")
    mem_count = len(bot.users)
    print(f'{bot.user.name} is now online in {server_count} server(s)')

@bot.command()
async def s(ctx, *, text):
    print("she gon call me baby boo")
    if ctx.author.id in ownID:
        message = ctx.message
        await message.delete()
        return await ctx.send(text)

@bot.event
async def on_message(message):
    if message.author.id == 1483292322182725662:
        return
    await bot.process_commands(message)
    print("meow")
    text = message.content
    for i in bannable_words:
        if i in text.lower():
            try:
                await message.author.send(f"Your message (`{text}`) contained the word `{i}`. You cannot say that word in this server. Doing so again will result in a ban.")
            except:
                pass
            admin_channel = message.guild.get_channel(int(ADMIN_CHANNEL_ID))
            await admin_channel.send(f"<@{message.author.id}> was warned for the message: ```{text}``` due to containing the word `{i}`.")
            await message.delete()
            return
    for i in swear_words:
        if i in text.lower():
            try:
                await message.author.send(f"Your message (`{text}`) contained the word `{i}`. This server is family friendly; please try to keep things clean!")
            except:
                pass
            await message.delete()
            return
        
    if "discord.gg" in text.lower() or "https://" in text.lower() or "http://" in text.lower():
        print("this part works")
        finger_painter_role = message.guild.get_role(FINGER_PAINTER_ROLE_ID)
        illustrator_role = message.guild.get_role(ILLUSTRATOR_ROLE_ID)
        promotion_forum = message.guild.get_channel(PROMOTION_FORUM_ID)
        if not finger_painter_role in message.author.roles and not illustrator_role in message.author.roles and not message.channel in promotion_forum.threads:
            try:
                await message.author.send(f"Your message (`{text}`) contained a link. Only finger painters and illustrators are allowed to send links in this server, so your message has been deleted. Thank you for understanding!\n-# If this was done in error, please contact a staff member from the Find the Finger Painters server for support.")
            except:
                pass
            await message.delete()
    if message.channel.id == CREATOR_UPDATES_CHANNEL_ID:
        finger_painter_role = message.guild.get_role(int(FINGER_PAINTER_ROLE_ID))
        illustrator_role = message.guild.get_role(int(ILLUSTRATOR_ROLE_ID))
        if finger_painter_role in message.author.roles or illustrator_role in message.author.roles:
            updates_role = message.guild.get_role(int(CREATOR_UPDATES_ROLE_ID))
            members = updates_role.members
            message_url = message.jump_url
            em = nextcord.Embed(
                title=f"{message.author.display_name} Just Posted a New Update!\n", color=nextcord.Color(int("CC99FF", 16)))
            em.add_field(name=f'"{message.content}"',
                            value=f"You can view it [here!]({message_url})", inline=False)
            member_url = message.author.avatar.url
            em.set_thumbnail(url=member_url)
            for member in members:
                await member.send(embed=em)
    

@bot.event
async def on_member_join(member):
    welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    background = Editor(Canvas((1200, 500)))
    try:
        profile_picture = await load_image_async(str(member.avatar.url))
    except:
        with Image.open(r"resources\images\defaultpfp.png") as pfp:
            profile_picture = Editor(pfp)
    profile = Editor(profile_picture).resize((187, 187))
    background.paste(profile, (507, 70))    
    with Image.open(r"resources\images\fpjointemplate.png") as fpjoinpic:
            fpjoin = Editor(fpjoinpic).resize((1200,500))
    background.paste(fpjoin, (0,0))
    poor_family_font = ImageFont.truetype(r"resources\fonts\PoorStory-Regular.ttf", 50)
    background.text((1200/2, 280), f"@{member.name}", font=poor_family_font, align="center")
    background.text((1200/2, 335), f"You are user: #{member.guild.member_count}", font=poor_family_font, align="center")
    background.text((1200/2, 390), f"Welcome to Find The Finger Painters!", font=poor_family_font, align="center")
    file = nextcord.File(fp=background.image_bytes, filename="joinfp.png")
    await welcome_channel.send(f"Welcome to the server, **{member.mention}**!",file=file)

    community_role = member.guild.get_role(COMMUNITY_ROLE_ID)
    await member.add_roles(community_role)

bot.run(TOKEN)