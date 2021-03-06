from discord.ext import commands
from pathlib import Path
import subprocess
import psutil
import discord
from colour import Color
import requests

# ======================================================
#
# ADD "token.txt" WITH YOUR BOT TOKEN TO RUN THE BOT!!!
# (it is added to .gitignore so that you won't commit it)
# (if its not added. ADD IT!)
#
# ======================================================

jackDiscordId = 276462585690193921

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


# UNFORTUNATELY WHEN THIS SCRIPT/COMMAND IS RUN BY PYTHON IT DOESN'T SHOW THE RIGHT RESULS
# EXAMPLES
@bot.command()
async def get_cpu_usageExample(ctx):
    output = subprocess.run(["./cpuUsage.sh"], shell=True)
    print("output: "+str(output.stdout))
    await ctx.channel.send("Current cpu usage is: "+str(output)+"%")

@bot.command()
async def get_cpu_usageExample2(ctx):
    output = subprocess.run(["grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"],stdout=subprocess.PIPE, shell=True)
    print("output: "+str(output.stdout))
    await ctx.channel.send("Current cpu usage is: "+str(output.stdout)+"%")
# FINISH EXAMPLES

# USE PYTHON LIBRARY INSTEAD
@bot.command()
async def get_cpu_usage(ctx):
    usage = psutil.cpu_percent()
    await ctx.channel.send("Current CPU usage is: "+str(usage)+"%")

@bot.command()
async def cpu_embed(ctx):
    # get cpu usage
    usage = psutil.cpu_percent()
    # create a list of colors from green to red. 100 different shades
    color_list = list(Color("green").range_to(Color("red"),100))
    # get color accordingly to cpu usage
    color = int("0x"+str(color_list[int(usage)])[1:], 16)
    # send embed message to chat
    embed = discord.Embed(
            title="CPU Usage",
            description=f"Current CPU usage is: {usage}% ",
            colour = discord.Colour(color)
        )
    await ctx.channel.send(embed=embed)

@bot.command()
async def system_info(ctx):
    if ctx.message.author.id == jackDiscordId:
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        values = psutil.virtual_memory()
        total = values.total >> 20
        available = values.available >> 20
        color_list = list(Color("green").range_to(Color("red"),100))
        color = int("0x"+str(color_list[int(cpu_usage)])[1:], 16)
        embed = discord.Embed(
                title="System usage information",
                colour = discord.Colour(color)
            )
        embed.add_field(name="CPU", value=f"Current CPU usage is: {cpu_usage}%")
        #embed.add_field(name="RAM", value=f"Current RAM usage is: {ram_usage}%")
        embed.add_field(name="RAM", value=f"Current RAM usage is: {total-available}/{total}MB")
        await ctx.channel.send(embed=embed)

@bot.command()
async def set_volume(ctx, volume):
    output = subprocess.run(["../volume.sh set_volume "+volume], shell=True)
    embed = discord.Embed(
            title="Sound volume",
            description=f"Volume has been set to {volume}%",
            colour = discord.Colour(0x1FE4FF)
        )
    await ctx.channel.send(embed=embed)

@bot.command()
async def set_volume2(ctx, volume):
    output = subprocess.run(["amixer sset -q 'Master' "+volume], shell=True)
    embed = discord.Embed(
            title="Sound volume",
            description=f"Volume has been set to {volume}%",
            colour = discord.Colour(0x1FE4FF)
        )
    await ctx.channel.send(embed=embed)

@bot.command()
async def get_volume(ctx):
    # output = subprocess.run(["../volume.sh get_volume"], shell=True)
    try:
        output = subprocess.check_output("../volume.sh get_volume", stderr=subprocess.STDOUT, shell=True).decode('ascii')
    # do something with output
    except subprocess.CalledProcessError:
        print(output)
    embed = discord.Embed(
            title="Sound volume",
            description=f"Volume is set to {output}%",
            colour = discord.Colour(0x1FE4FF)
        )
    await ctx.channel.send(embed=embed)

@bot.command()
async def av(ctx):
    embed = discord.Embed(
            title="user",
            colour = discord.Colour(0x1FE4FF)
        )
    embed.set_image(url=ctx.message.author.avatar_url)
    await ctx.channel.send(embed=embed)

@bot.command()
async def run_command(ctx, *command):
    try:
        output = subprocess.check_output(" ".join(command[:]), stderr=subprocess.STDOUT, shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        print(output)
    embed = discord.Embed(
            title="Command output",
            description=f"{output}",
            colour = discord.Colour(0x1FE4FF)
        )
    await ctx.channel.send(embed=embed)

@bot.command()
async def ask_admin(ctx):
    answer = input(str(ctx.author)+" asked you something, type response: ")
    embed = discord.Embed(
            title="Admin response",
            description=str(answer),
            colour = discord.Colour(0xFF0000)
        )
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount):
    amount = int(amount)
    if amount <= 100:
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.channel.send('Cannot delete more than 100 messages at a time!')

@bot.command()
async def githubAPI(ctx, githubUser):
    response = requests.get("https://api.github.com/users/"+githubUser)
    json_response = response.json()
    embed = discord.Embed(
            title=json_response['login'],
            colour = discord.Colour(0xFFFFFF)
            # set_image(url=json_response['avatar_url'])
        )
    # embed.set_image(url=json_response['avatar_url'])
    embed.add_field(name="Blog", value=json_response['blog'])
    await ctx.channel.send(embed=embed)

file = open(Discord_Bot_Dir / 'token.txt','rt')
bot.run(str(file.read()))