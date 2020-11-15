import discord
from discord.ext import commands
import json
import os
import random
import time

os.chdir("C:\\Users\\DRE\\Desktop\\economy bot")

client = commands.Bot(command_prefix="l!")

@client.event
async def on_ready():
    print("bot is now ready")

@client.command(aliases=["bal"])
async def balance(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()
    wamt = users[str(user.id)]["wallet"]
    bamt = users[str(user.id)]["bank"]

    embed = discord.Embed(title= f"{ctx.author.name}'s balance", timestamp=ctx.message.created_at)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    embed.add_field(name="Wallet", value=wamt)
    embed.add_field(name="Bank", value=bamt)

    await ctx.send(embed=embed)

@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earn = random.randrange(500)

    await ctx.send(f"Bill cosby gave you {earn} coins!")

    users[str(user.id)]["wallet"] += earn

    with open("economy.json", "w") as f:
        json.dump(users, f)




async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    
    with open("economy.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("economy.json", "r") as f:
        users = json.load(f)
    
    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("economy.json", "w") as f:
        json.dump(users, f)

        bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal

@client.command()
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("You cannot withdraw nothing!")
        return
    
    
    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = await update_bank(ctx.author, "bank")[0]

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send("You are too broke for this")
        return
    
    if amount < 0:
        await ctx.send("You cannot do that dud.")
        return
    
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")

    await ctx.send(f"You withdrew {amount} coins!")

@client.command(aliases=["dep"])
async def deposit(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("You cannot withdraw nothing!")
        return
    
    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send("You are too broke for this")
        return
    
    if amount < 0:
        await ctx.send("You cannot do that dud.")
        return
    
    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author, amount, "bank")

    await ctx.send(f"You deposited {amount} coins!")

@client.command(aliases=["send"])
async def give(ctx, member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("You cannot withdraw nothing!")
        return
    
    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send("You are too broke for this")
        return
    
    if amount < 0:
        await ctx.send("You cannot do that dud.")
        return
    
    await update_bank(ctx.author, -1*amount, "bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"You gave {amount} coins to {member}!")

@client.command()
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("You cannot withdraw nothing!")
        return
    
    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send("You are too broke for this")
        return
    
    if amount < 0:
        await ctx.send("You cannot do that dud.")
        return
    
    final = []
    
    for i in range(3):
        a= random.choice(["😍", "😎", "🤑"])

        final.append(a)
    
    await ctx.send(str(final))

    if final[0] == final[1] or  final[0] or final[2] or final[2] == final[1]:
        await update_bank(ctx.author, 5*amount)
        await ctx.send("YOU WON!1!!11!1!")
    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.send("You lost, you bum!")

@client.command(aliases=["steal"])
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)


    
    bal = await update_bank(member)

    if bal[1] < 100:
        await ctx.send("Do not rob this guy, he is broke af!")
        return
    
    earnings = random.randrange(0, bal[0])
    
    await update_bank(ctx.author, earnings)
    await update_bank(member, -1*earnings)

    await ctx.send(f"You robbed {earnings} coins from {member}!")



client.run("")
