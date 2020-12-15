import json
import os
import discord
from discord.ext import commands

bot=commands.Bot(command_prefix=commands.when_mentioned_or(".s ")
                ,description="Test Description"
                ,case_insensative=True
                ,intents=discord.Intents().all())
bot.remove_command("help")
###########################################################################
@bot.event #Loads all cogs and initiates bot
async def on_ready():
    
    cogList=["fun","misc", "mod"]
    
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
            await sysChannel.send("Sup bitches, i'm here to fuck shit up... since y'all are uneducated, type *.s help -f* to learn some stuff about me... if you dare :expressionless:")
        except Exception as error:
            print (error)
###########################################################################
@bot.event #Sends a message when someone joins the server
async def on_member_join(member):
    sysChannel=member.guild.system_channel
    if sysChannel:
        await sysChannel.send("Well well well... look who joined... welcome to hell "+member.mention)
###########################################################################
@bot.event #Sends a message when someone leaves the server
async def on_member_remove(member):
    sysChannel=member.guild.system_channel
    if sysChannel:
        await sysChannel.send("Adios "+member.mention+"... \t\t\t\t\t\t\t\t\t\t\t**asshole**")
###########################################################################
@bot.command(name="help") #Help messages
async def help(ctx, arg: str=""):
    helpEmbed=discord.Embed(title="Sentinel Prefix: **.s**",color=discord.Color.green())
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
        await ctx.send(ctx.message.author.mention+", guess what? You typed it wrong *dipshit*, use *.s help -f* for an extensive guide or *.s help -s* for a short guide")
###########################################################################
'''@bot.event
async def on_message(message):
    if message.author==bot.user: #Ensures bot doesn't respond to itself
        return
    
    if message.content.startswith("hi"):
        await message.channel.send("Hello @"+str(message.author.mention))

    await bot.process_commands(message) #Enables commands'''
###########################################################################
bot.run(os.environ["DISCORDTOKEN"])
