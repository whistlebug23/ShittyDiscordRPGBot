import random
# import os
import discord
from discord.ext import commands
import sqlite3

db_path = "CorporateQuestsGameData.db"
con = sqlite3.connect(db_path)
cursor = con.cursor()

# ---------------------------
# FUNCTIONS
# ---------------------------


async def update_player_class(ctx_in, class_name):
    if ctx_in.channel.id == 962738344880668702:  # Check to see if the user is in The Stronghold
        member = ctx_in.message.author
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except discord.HTTPException:
                print(f"Can't remove the role {i}")
        role = discord.utils.get(member.guild.roles, name=class_name)
        await member.add_roles(role, atomic=True)
        sql_user_role_updt_params = (str(class_name), int(member.id))
        cursor.execute(sql_user_role_updt, sql_user_role_updt_params)
        con.commit()
    else:
        await ctx_in.send("You must be in The Stronghold to change classes!")


async def update_player_wap(ctx_in, combat_message, wap_value):
    member = ctx_in.message.author
    if ctx_in.channel.id in safe_channels:  # Check to see if the user is in a safe text channel
        await ctx_in.send("There be no combat in here! Take that outside.")
    else:
        await ctx_in.send(f"{combat_message} WAP {str(wap_value)}")
        sql_wap_updt_params = (int(wap_value), int(member.id))
        cursor.execute(sql_wap_updt, sql_wap_updt_params)
        con.commit()

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
        print(f"{self.player_name}'s health is {self.player_health}")

# p1 = CQPlayer(1, "Carl", "Nekro", 100)

# print(p1.player_name)
# print(p1.player_health)
# p1.print_health()


with open("bot_token.txt", "r") as file:
    TOKEN = file.read().rstrip()

GUILD = "Discord Bot Testing"

intents = discord.Intents.all()
client = discord.Client(intents=intents)
intents.members = True
bot = commands.Bot(command_prefix=("!", "/", "*"), intents=intents)

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


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    sql_user = "INSERT OR IGNORE INTO CQPlayers values(?, ?, ?, ?);"
    for guild in bot.guilds:
        for member in guild.members:
            if member.bot == 0:
                sql_params = (int(member.id), str(member.name), str(member.top_role), 45)
                cursor.execute(sql_user, sql_params)
                con.commit()
            else:
                return


@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(", ".join(dice))


# ---------------------------
# CHANGE CLASS MECHANICS
# ---------------------------
# TODO: Info command

# ---------------------------
# CHANGE CLASS MECHANICS
# ---------------------------
sql_user_role_updt = "UPDATE CQPlayers SET PlayerClass = ? WHERE DiscordID = ?;"


@bot.command(name="HarryWiz", help="Grants user Harry Wizard Role")
@commands.check(normal_prefix)
async def add_role(ctx):
    user_role = "Harry Wizard"
    await update_player_class(ctx, user_role)


@bot.command(name="Orx", help="Grants user Orx Role")
@commands.check(normal_prefix)
async def add_role(ctx):
    user_role = "Orx"
    await update_player_class(ctx, user_role)


@bot.command(name="Nekro", help="Grants user Nekromancer Role")
@commands.check(normal_prefix)
async def add_role(ctx):
    user_role = "Nekromancer"
    await update_player_class(ctx, user_role)

# ---------------------------
# COMBAT MECHANICS
# ---------------------------
sql_wap_updt = "UPDATE CQPlayers SET PlayerWap = PlayerWap+? WHERE DiscordID = ?;"


@bot.command(name="notmyprob", help="For when you do something that's not your job (1d4).")
@commands.check(combat_prefix)
async def combat_notmyproblem(ctx):
    notmyproblem_msg = "Did something that wasn't your job?"
    notmyproblem_dmg = random.choices(range(1, 5), weights=(40, 35, 20, 5))[0]
    await update_player_wap(ctx, notmyproblem_msg, notmyproblem_dmg*-1)


@bot.command(name="coworker_aggro", help="For when your co-worker drags you into something (1d6).")
@commands.check(combat_prefix)
async def combat_cwkraggro(ctx):
    cwkraggro_msg = "Got dragged into something?"
    cwkraggro_dmg = random.choices(range(1, 7), weights=(10, 15, 25, 25, 15, 10))[0]
    await update_player_wap(ctx, cwkraggro_msg, cwkraggro_dmg*-1)


# ---------------------------
# HEALING MECHANICS
# ---------------------------


@bot.command(name="ale", help="Imbibe some ale for what ails you (1d6).")
@commands.check(heal_prefix)
async def heal_ale(ctx):
    if ctx.channel.id == 962738344880668702:  # Check to see if the user is in the Stronghold
        await ctx.send("You can't drink here, that's what the Tavern is for.")
    else:
        if ctx.channel.id in combat_channels:
            await ctx.send("I mean, don't drink too much out here...")
        ale_heal_amt = str(*random.choices(range(1, 7), weights=(25, 20, 20, 20, 10, 5)))
        await ctx.send("Take a swig, it'll help. Probably. WAP+" + ale_heal_amt)

bot.run(TOKEN)
