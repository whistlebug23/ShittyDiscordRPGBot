import random
import os
import discord
from discord.ext import commands
import sqlite3

db_path = "CorporateQuestsGameData.db"

# ---------------------------
# PLAYER CLASS
# ---------------------------
class CQPlayer:
    def __init__(self, player_id: int, player_name: str, player_class: str, player_health: int):
        self.player_id = player_id
        self.player_name = player_name
        self.player_class = player_class
        self.player_health = player_health

    def print_health(self):
        print(f"{self.player_name}\'s health is {self.player_health}")


p1 = CQPlayer(1, "Carl", "Nekro", 100)


print(p1.player_name)
print(p1.player_health)
p1.print_health()

with open('bot_token.txt', 'r') as file:
    TOKEN = file.read().rstrip()

GUILD = 'Discord Bot Testing'

intents = discord.Intents.all()
client = discord.Client(intents=intents)
intents.members = True
bot = commands.Bot(command_prefix=('!', '/', '*'), intents=intents)

# These are text channels where combat cannot occur
safe_channels = [962738344880668702, 962773311606112266]

# These are text channels where combat can occur
combat_channels = [962754186632630282]


def normal_prefix(ctx):
    return ctx.prefix == "!"


def combat_prefix(ctx):
    return ctx.prefix == "/"


def heal_prefix(ctx):
    return ctx.prefix == "*"


sql_user = "INSERT OR IGNORE INTO CQPlayers values(?, ?, ?, ?);"


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    for guild in bot.guilds:
        for member in guild.members:
            if member.bot == 0:
                sql_params = (str(member.id), str(member.name), str(member.top_role), 45)

                print(member.id)
                print(member.name)
                print(member.top_role)

                con = sqlite3.connect(os.path.abspath(db_path))
                cursor = con.cursor()
                cursor.execute(sql_user, sql_params)
                con.commit()
                con.close()
            else:
                return


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


# ---------------------------
# CHANGE CLASS MECHANICS
# ---------------------------
# TODO: Info command

# ---------------------------
# CHANGE CLASS MECHANICS
# ---------------------------
@bot.command(name='HarryWiz', help='Grants user Harry Wizard Role')
@commands.check(normal_prefix)
async def addrole(ctx):
    if ctx.channel.id == 962738344880668702:  # Check to see if the user is in The Stronghold
        member = ctx.message.author
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i}")
        role = discord.utils.get(member.guild.roles, name="Harry Wizard")
        await member.add_roles(role, atomic=True)
    else:
        await ctx.send("You must be in The Stronghold to change classes!")


@bot.command(name='Orx', help='Grants user Orx Role')
@commands.check(normal_prefix)
async def addrole(ctx):
    if ctx.channel.id == 962738344880668702:  # Check to see if the user is in The Stronghold
        member = ctx.message.author
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i}")
        role = discord.utils.get(member.guild.roles, name="Orx")
        await member.add_roles(role, atomic=True)
    else:
        await ctx.send("You must be in The Stronghold to change classes!")


@bot.command(name='Nekro', help='Grants user Nekromancer Role')
@commands.check(normal_prefix)
async def addrole(ctx):
    if ctx.channel.id == 962738344880668702:  # Check to see if the user is in The Stronghold
        member = ctx.message.author
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i}")
        role = discord.utils.get(member.guild.roles, name="Nekromancer")
        await member.add_roles(role, atomic=True)
    else:
        await ctx.send("You must be in The Stronghold to change classes!")

# ---------------------------
# COMBAT MECHANICS
# ---------------------------
@bot.command(name='notmyprob', help='For when you do something that\'s not your job (1d4).')
@commands.check(combat_prefix)
async def combat_notmyproblem(ctx):
    if ctx.channel.id in safe_channels:  # Check to see if the user is in a safe text channel
        await ctx.send("There be no combat in here! Take that outside.")
    else:
        notmyproblem_dmg = str(*random.choices(range(1, 5), weights=(40, 35, 20, 5)))
        await ctx.send('Did something that was not your job? WAP-' + notmyproblem_dmg)

@bot.command(name='coworker_aggro', help='For when your co-worker drags you into something (1d6).')
@commands.check(combat_prefix)
async def combat_cwkraggro(ctx):
    if ctx.channel.id in safe_channels:  # Check to see if the user is in a safe text channel
        await ctx.send("There be no combat in here! Take that outside.")
    else:
        cwkraggro_dmg = str(*random.choices(range(1, 7), weights=(10, 15, 25, 25, 15, 10)))
        await ctx.send('Got dragged into something? WAP-' + cwkraggro_dmg)

# ---------------------------
# HEALING MECHANICS
# ---------------------------
@bot.command(name='ale', help='Imbibe some ale for what ails you (1d6).')
@commands.check(heal_prefix)
async def heal_ale(ctx):
    if ctx.channel.id == 962738344880668702:  # Check to see if the user is in the Stronghold
        await ctx.send("You can\'t drink here, that\'s what the Tavern is for.")
    else:
        if ctx.channel.id in combat_channels:
            await ctx.send("I mean, don\'t drink too much out here...")
        ale_heal_amt = str(*random.choices(range(1, 7), weights=(25, 20, 20, 20, 10, 5)))
        await ctx.send('Take a swig, it\'ll help. Probably. WAP+' + ale_heal_amt)


bot.run(TOKEN)