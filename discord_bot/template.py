from discord.ext import commands
from pathlib import Path
import subprocess

# ======================================================
#
# ADD "token.txt" WITH YOUR BOT TOKEN TO RUN THE BOT!!!
# (it is added to .gitignore so that you won't commit it)
#
# ======================================================

bot = commands.Bot(command_prefix="<")
#bot.remove_command('help')
Discord_Bot_Dir = Path(__file__).parent.absolute()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def hello(ctx):
    if ctx.message.author == bot.user:
        return
    else:
        await ctx.channel.send('Hello!')

# @bot.command()
# async def hello2(ctx):
#     Bot=subprocess.run(["awk -F'[]%[]' '/dB/ {print $2}' <(amixer sget Master)"],stdout=subprocess.PIPE, shell=true)
#     print(str(Bot.stdout))

@bot.command()
async def hello2(ctx):
    Bot=subprocess.Popen("awk -F'[]%[]' '/dB/ {print $2}' <(amixer sget Master)", shell=True, executable="/bin/bash")
    print(str(Bot.stdout))

file = open(Discord_Bot_Dir / 'token.txt','rt')
bot.run(str(file.read()))