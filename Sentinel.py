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
@bot.command(name="help") #Help messages
async def help(ctx, arg: str=""):
    helpEmbed=discord.Embed(title="Sentinel Prefix: **.s**\t\tKey: ()=required; []=optional",color=discord.Color.green())
    helpEmbed.set_author(name="An Idiot's Guide to Sentinel")
    helpEmbed.set_footer(text="Some moron named PureCache made me")

    if arg.strip().lower()=="-f": #Full version
        
        with open("SentinelHelp.json","r") as helpFile:
            data=json.load(helpFile)
        data=data["full"]

        for key in data:
            value=("\n".join(x for x in data[key]))
            helpEmbed.add_field(name=key,value=f"```{value}```",inline=False)
    
    elif arg.strip().lower()=="-s": #Short version
        with open("SentinelHelp.json", "r") as helpFile:
            data = json.load(helpFile)
        data = data['short']
        for key in data:
            helpEmbed.add_field(name=key, value=data[key], inline=False)
    
    else: #Defaults to short version
        with open("SentinelHelp.json", "r") as helpFile:
            data = json.load(helpFile)
        data = data['short']
        for key in data:
            helpEmbed.add_field(name=key, value=data[key], inline=False)
    
    
    try:
        await ctx.send("So you decided to ask for help... well here it is ya' brat")
        await ctx.send(embed=helpEmbed)
    except Exception as error:
        print (error)

@help.error
async def clear_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(ctx.message.author.mention+", guess what? You typed it wrong *dipshit*, use *.s help -f* for an extensive guide or *.s help* for a short guide")
###########################################################################
'''@bot.event
async def on_message(message):
    if message.author==bot.user: #Ensures bot doesn't respond to itself
        return
    
    if message.content.startswith("hi"):
        await message.channel.send("Hello @"+str(message.author.mention))

    await bot.process_commands(message) #Enables commands'''
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
