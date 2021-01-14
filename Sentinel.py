import psycopg2
import json
from configparser import ConfigParser
import os
import discord
from discord.ext import commands

bot=commands.Bot(command_prefix=commands.when_mentioned_or(".s ")
                ,case_insensative=True
                ,owner_id=338707493188272129
                ,intents=discord.Intents().all())
bot.remove_command("help")
###########################################################################
@bot.event #Loads all cogs and initiates bot
async def on_ready():
    
    with open("SentinelHelp.json","r") as cogFile:
        data=json.load(cogFile)
    data=data["Cogs"]
    cogList=list(data.keys())
    
    for cog in cogList:
        cog=("Cogs."+cog)
        try:
            bot.load_extension(cog)
            print ("Loaded",cog)
        except Exception as e:
            print ("Error loading",cog,"e:",e)

    await bot.change_presence(activity=discord.Game(name="with Cache's emotions"))
    print (bot.user.name,"successfully connected to Discord")
###########################################################################
@bot.event #Sends message when bot joins server
async def on_guild_join(guild):
    sysChannel=guild.system_channel
    if sysChannel:
        try:
            await sysChannel.send("Sup bitches, i'm here to fuck shit up... since y'all are uneducated, type *.s help* to learn some stuff about me... if you dare :expressionless:")
        except Exception as error:
            print (error)
###########################################################################
@bot.event #Sends a message when someone joins the server
async def on_member_join(member):
    sysChannel=member.guild.system_channel
    if sysChannel:
        await sysChannel.send("Well well well... look who joined... welcome to hell "+member.mention)
        embed=discord.Embed()
        embed.set_image(url="https://media.tenor.co/images/3ccff8c4b2443d93811eac9b2fd56f11/raw")
        await sysChannel.send(embed=embed)
###########################################################################
@bot.event #Sends a message when someone leaves the server
async def on_member_remove(member):
    embed=discord.Embed()
    for channel in member.guild.text_channels:
        if isinstance(channel, discord.TextChannel):
            if "goodbye" in str(channel):
                await channel.send("Adios **"+str(member)+"**... \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t")
                embed.set_image(url="https://media.giphy.com/media/ef0ZKzcEPOBhK/giphy.gif")
                await channel.send(embed=embed)
                return
    sysChannel=member.guild.system_channel
    if sysChannel:
        await sysChannel.send("Adios **"+str(member)+"**... \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t")
        embed.set_image(url="https://media.giphy.com/media/ef0ZKzcEPOBhK/giphy.gif")
        await sysChannel.send(embed=embed)
###########################################################################
@bot.command(name="help", aliases=["h","helpinfo"]) #Help messages
async def help(ctx, type=None):
    if type==None:
        with open("SentinelHelp.json", "r") as helpFile:
            data = json.load(helpFile)
        data = data['short']
        
        embed=discord.Embed(title="An Idiot's Guide to Sentinel\t\tPrefix: .s",color=discord.Color.green())
        embed.set_author(name="Type `.s [category]` to see an in-depth guide for the inputed category")
        embed.set_footer(text="Some moron named PureCache made me")
        embed.add_field(name="Fun Commands",value=data["Fun"],inline=False)
        embed.add_field(name="Game Commands",value=data["Games"],inline=False)
        embed.add_field(name="Utility Commands",value=data["Utility"],inline=False)
        embed.add_field(name="Roles Commands",value=data["Roles"],inline=False)
        embed.add_field(name="Miscellaneous Commands",value=data["Miscellaneous"],inline=False)
        embed.add_field(name="Mod Commands",value=data["Mod"],inline=False)
    
    else:
        with open("SentinelHelp.json","r") as helpFile:
            data=json.load(helpFile)
        data=data["full"]
        data=data[type.lower()]
        embed=discord.Embed(title=(f"{type.lower()} commands:"),color=discord.Color.green())
        embed.set_author(name=("Key: (required) [optional]"))
        embed.set_footer(text="Some moron named PureCache made me")

        for key in data:
            embed.add_field(name=(f"`{key}`"),value=data[key],inline=False)
    
    await ctx.send(embed=embed)

@help.error
async def clear_error(ctx,error):
    await ctx.send("This category does not exist! Make sure you spelled it correctly, use `.s help` to see a short list of all types")
###########################################################################
@bot.event #If user just types in '.s'
async def on_message(message):
    if message.author==bot.user: #So bot doesn't respond to itself
        return
    
    if message.content==".s":
        await message.channel.send(f"Hello {message.author.mention}! Use `.s help` to learn more about me!")

    await bot.process_commands(message) #Enables commands
###########################################################################
try:
    conn=psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
    print ("Database connection established from environment")
except:
    config_object=ConfigParser()
    config_object.read("SentinelVariables.ini")
    variables=config_object["variables"]
    DATABASE_URL=variables["DATABASE_URL"]
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    print ("Database connection established from .ini")
try:
    bot.run(os.environ["DISCORDTOKEN"])
except:
    config_object=ConfigParser()
    config_object.read("SentinelVariables.ini")
    variables=config_object["variables"]
    DISCORD_TOKEN=variables["DISCORD_TOKEN"]
    bot.run(DISCORD_TOKEN)
