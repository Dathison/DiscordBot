import subprocess
import secrets
import discord
from discord.ext import commands

TOKEN = secrets.discord_token

description = '''Piss Bot for the Piss people!'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def piss(ctx):
    """Says world"""
    await ctx.send("Hello world!")


@bot.command()
async def add(ctx, left : int, right : int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def subtract(ctx, left : int, right : int):
    """Subtracts two numbers.."""
    await ctx.send(left - right)

@bot.command()
async def multiply(ctx, left : int, right : int):
    """Multiples two numbers"""
    await ctx.send(left * right)

@bot.command()
async def divide(ctx, left : int, right : int):
    """Divides two numbers."""
    if left == 0 or right == 0:
        await ctx.send("Don't fucking divide by zero, you idiot.")
    else:
        await ctx.send(left / right)
        return

#@bot.event
#async def on_message(message):
#	username = str(message.author).split("#")[0]
#	channel = str(message.channel.name)
#	user_message = str(message.content)
#
#	print(f'{username} said: {user_message} in {channel}')
#
#	if message.author == bot.user:
#		return

@bot.command()
async def pl_table(ctx):

    "Shows the Premier League table of the current season."

	#table_proc = subprocess.Popen([table.py], stdout=subprocess.PIPE)
	#print(stdout)
    table_output = open("table_output","r")
    await ctx.send(table_output.read())

bot.run(TOKEN)
