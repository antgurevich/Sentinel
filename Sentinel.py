import json
import random
from configparser import ConfigParser
import os
import discord
from discord.ext import commands

from Cogs.db import dbconnect

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

    randNum=random.randint(1,5)
    if randNum==1:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Cache be a Moron [.s]"))
    elif randNum==2:
        await bot.change_presence(activity=discord.Game("with Cache's Emotions [.s]"))
    elif randNum==3:
        await bot.change_presence(activity=discord.Streaming(name="Idiot Simulator [.s]", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO"))
    elif randNum==4:
        await bot.change_presence(activity=discord.Game("with ur mom [.s]"))
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Cache's bullshit [.s]"))
    print (bot.user.name,"successfully connected to Discord")
###########################################################################
@bot.event #Sends message when bot joins server
async def on_guild_join(guild):
    cursor,conn=dbconnect() #Opens connection to db
    
    sql=("SELECT guild_id, reason FROM banned_entities WHERE guild_id=%s;")
    cursor.execute(sql, (guild.id,))
    result=cursor.fetchone()
    
    conn.close() #Closes connection to db
    sysChannel=guild.system_channel
    if result is None:
        await sysChannel.send(embed=discord.Embed(title="Sup nerds... type *.s help* to learn some stuff about me... if you dare :expressionless:"))
    elif result[0]==guild.id:
        await sysChannel.send(embed=discord.Embed(title=f"This server was blacklisted from the bot! Reason: {result[1]}. Contact PureCache#0001 for an appeal"))
        guild=bot.get_guild(guild.id)
        await guild.leave()
        return
###########################################################################
@bot.event #Sends a message when someone joins the server
async def on_member_join(member):
    cursor,conn=dbconnect() #Opens connection to db

    sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
    cursor.execute(sql, (member.guild.id, "welcome_channel"))
    result=cursor.fetchone()
    if result is not None: #Custom channel
        channel=member.guild.get_channel(int(result[0]))
    else: #System channel
        channel=member.guild.system_channel

    sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
    cursor.execute(sql, (member.guild.id,"welcome_status"))
    result=cursor.fetchone()
    
    if result is None or result[0]=="True": #welcome_status does not exist or is true
        sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
        cursor.execute(sql, (member.guild.id,"welcome_msg"))
        result=cursor.fetchone()
        if result is None: #Custom welcome message does not exist
            message="Well well well... look who joined... welcome to hell %s"
        else: #Custom message does exist
            message=result[0]
        sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
        cursor.execute(sql, (member.guild.id,"welcome_picture"))
        result=cursor.fetchone()
        if result is None: #default url
            url="https://media.tenor.co/images/3ccff8c4b2443d93811eac9b2fd56f11/raw"
        else: #Custom url for image
            url=result[0]
        
        await channel.send(message %member.mention)
        embed=discord.Embed()
        embed.set_image(url=url)
        await channel.send(embed=embed)
    conn.close() #Closes connection to db
###########################################################################
@bot.event #Sends a message when someone leaves the server
async def on_member_remove(member):
    cursor,conn=dbconnect() #Opens connection to db
    
    sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
    cursor.execute(sql, (member.guild.id, "leave_channel"))
    result=cursor.fetchone()
    if result is not None:
        channel=member.guild.get_channel(int(result[0]))
    else:
        channel=member.guild.system_channel

    sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
    cursor.execute(sql, (member.guild.id,"leave_status"))
    result=cursor.fetchone()
    
    if result is None or result[0]=="True": #welcome_status does not exist or is true
        sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
        cursor.execute(sql, (member.guild.id,"leave_msg"))
        result=cursor.fetchone()
        if result is None: #Custom welcome message does not exist
            message="Adios %s..."
        else: #Custom message does exist
            message=result[0]
        sql=("SELECT setting_value FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
        cursor.execute(sql, (member.guild.id,"leave_picture"))
        result=cursor.fetchone()
        if result is None: #default url
            url="https://media.giphy.com/media/ef0ZKzcEPOBhK/giphy.gif"
        else: #Custom url for image
            url=result[0]
        await channel.send(message %member)
        embed=discord.Embed()
        embed.set_image(url=url)
        await channel.send(embed=embed)
    conn.close() #Closes connection to db
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
        embed.add_field(name="Settings Commands",value=data["Settings"],inline=False)
    
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
    await ctx.send(embed=discord.Embed(title="This category does not exist! Make sure you spelled it correctly, use `.s help` to see a short list of all types"))
###########################################################################
@bot.event #If user just types in '.s'
async def on_message(message):
    if message.author==bot.user: #So bot doesn't respond to itself
        return
    
    if message.content==".s":
        await message.channel.send(embed=discord.Embed(title=f"Hello {message.author}! Use `.s help` to learn more about me!"))

    await bot.process_commands(message) #Enables commands
###########################################################################
@bot.check #Checks for blacklisted users
async def blacklist_check(ctx):
    try:
        cursor,conn=dbconnect() #Opens connection to db
        sql=("SELECT user_id, reason FROM banned_entities WHERE user_id=%s;")
        cursor.execute(sql, (ctx.author.id,))
        result=cursor.fetchone()
        conn.close() #Closes connection to db
        
        if result is not None: #Blacklsited
            await ctx.send(embed=discord.Embed(title=f"You have been blacklisted from the bot for reason: {result[1]}! Contact PureCache#0001 to appeal!"))

        return result is None    
        
    except Exception as e:
        print (e)
###########################################################################
@bot.event #Generic error handling
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(title="Command not found! Use `.s help` for a list of all commands"))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(title="You are currently on cooldown!"))
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(embed=discord.Embed(title="I do not have permission to do that! Try enabling the proper permissions for me and trying again"))
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send(embed=discord.Embed(title="This command is only available in servers!"))
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(embed=discord.Embed(title="This command is currently disabled!"))
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(embed=discord.Embed(title="User not found! Make sure to correctly tag them"))
    elif isinstance(error, commands.NotOwner):
        await ctx.send(embed=discord.Embed(title="You're not the owner dummy, you can't use this"))
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send(embed=discord.Embed(title="You provided too many arguments! Check the help menu if you need help"))
###########################################################################
try:
    bot.run(os.environ["DISCORDTOKEN"])
except:
    config_object=ConfigParser()
    config_object.read("SentinelVariables.ini")
    variables=config_object["variables"]
    DISCORD_TOKEN=variables["DISCORDTOKEN"]
    bot.run(DISCORD_TOKEN)
