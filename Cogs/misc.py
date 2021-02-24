import asyncio
import json
import discord
from discord.ext import commands

from Cogs.db import dbconnect

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        cursor,conn=dbconnect() #Opens connection to db
        if before.author.id!=self.bot.user.id:
            message=before.content
            #author=str(before.author)[:-5]
            try:
                sql=('''SELECT * FROM yoink_command
                WHERE (guild_id=%s AND yoink_type=%s and channel_id=%s);''')
                cursor.execute(sql, (before.guild.id, "edit", before.channel.id))
                if cursor.fetchone() is None:
                    sql=('''INSERT INTO yoink_command(guild_id, user_id, channel_id, message_content, yoink_type)
                    VALUES (%s, %s, %s, %s, %s);''')
                    cursor.execute(sql, (before.guild.id, before.author.id, before.channel.id, message, "edit"))
                    conn.commit()
                else:
                    sql=('''UPDATE yoink_command
                    SET user_id=%s, message_content=%s
                    WHERE (guild_id=%s AND yoink_type=%s AND channel_id=%s);''')
                    cursor.execute(sql, (before.author.id, message, before.guild.id, "edit", before.channel.id))
                    conn.commit()
            except Exception as e:
                print (e)
        conn.close() #Closes connection to db                
    
    @commands.command(name="yoinkedit", aliases=["editsnipe","snipeedit","edityoink"])
    async def yoinkedit(self, ctx):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=('''SELECT * FROM yoink_command
                WHERE (guild_id=%s AND yoink_type=%s AND channel_id=%s);''')
            cursor.execute(sql, (ctx.guild.id, "edit", ctx.channel.id))
            results=cursor.fetchone()
            if results is None:
                await ctx.send(embed=discord.Embed(title="No one edited any messages!"))
                return
            else:
                message=results[4]
                author=str(self.bot.get_user(results[2]))[:-5]
                embed=discord.Embed(title=f"{author}'s Absolute :clown: Moment",color=discord.Color.orange())
                embed.add_field(name="Mans really tried to change",value=f"`{message}`")
                await ctx.send(embed=embed)
        except Exception as e:
            print (e)
        conn.close() #Closes connection to db
###########################################################################
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        cursor,conn=dbconnect() #Opens connection to db
        if message.author.id!=self.bot.user.id:
            try:
                sql=('''SELECT * FROM yoink_command
                WHERE (guild_id=%s AND yoink_type=%s and channel_id=%s);''')
                cursor.execute(sql, (message.guild.id, "delete", message.channel.id))
                if cursor.fetchone() is None:
                    sql=('''INSERT INTO yoink_command(guild_id, user_id, channel_id, message_content, yoink_type)
                    VALUES (%s, %s, %s, %s, %s);''')
                    cursor.execute(sql, (message.guild.id, message.author.id, message.channel.id, message.content, "delete"))
                    conn.commit()
                else:
                    sql=('''UPDATE yoink_command
                    SET user_id=%s, message_content=%s
                    WHERE (guild_id=%s AND yoink_type=%s AND channel_id=%s);''')
                    cursor.execute(sql, (message.author.id, message.content, message.guild.id, "delete", message.channel.id))
                    conn.commit()
            except Exception as e:
                print (e)
        conn.close() #Closes connection to db
    
    @commands.command(name="yoink", aliases=["snipe","deleted"])
    async def yoink(self, ctx):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=('''SELECT * FROM yoink_command
                WHERE (guild_id=%s AND yoink_type=%s AND channel_id=%s);''')
            cursor.execute(sql, (ctx.guild.id, "delete", ctx.channel.id))
            results=cursor.fetchone()
            if results is None:
                await ctx.send(embed=discord.Embed(title="No one deleted any messages!"))
                return
            else:
                author=str(self.bot.get_user(results[2]))[:-5]
                embed=discord.Embed(color=discord.Color.orange())
                embed.add_field(name="Imagine trying to delete a message :clown:",value=(f"**{author}:** `{results[4]}`"))
                await ctx.send(embed=embed)
        except Exception as e:
            print (e)
        conn.close() #Closes connection to db
###########################################################################
    @commands.command(name="changelog",aliases=["changes","updates"])
    async def changelog(self,ctx):
        logEmbed=discord.Embed(title="Sentinel Change Log",color=discord.Color.teal())
        
        with open("SentinelHelp.json","r") as logFile:
            data=json.load(logFile)
        data=data["changeLog"]
        for key in data:
            logEmbed.add_field(name=("*"+key+"*"),value=data[key],inline=False)
        
        await ctx.send(embed=logEmbed)   
###########################################################################
    @commands.command(name="purge", aliases=["clear","delete"]) #Clears previous x amount of messages (x between 1 & 50)
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int): 
        if limit>50 or limit<1:
            await ctx.send("Oi cunt! I can only clear between 1 & 50 messages at a time, y u entering something outside that range?!?!")
            return
        try:
            await ctx.message.channel.purge(limit=(limit+1))
            msg=await ctx.send("Previous "+str(limit)+" messages deleted")
            await asyncio.sleep(2)
            await msg.delete()
        except discord.Forbidden:
           await ctx.send("You didn't give me enough permissions dipshit. Give me `Manage Messages` permission headass")

    @purge.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("LLLLL you don't have permission to use this command. Sucks to suck doesn't it")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("I can only delete a certain **number** of messages, not a certain **word** of messages, dipshit. Use *.s purge [x]*")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Bro, you gotta enter an amount of messages to clear. Use *.s purge [x]* , smh my head")
###########################################################################
    @commands.command(name="botinfo", aliases=["info"]) #Displays informaton about Sentinel
    async def botinfo(self, ctx):
        infoDict={
                "Created": "December 2020"
                ,"Language": "Python 3.8.1"
                ,"Open Source GitHub": "https://github.com/antgurevich/Sentinel"
                }
        infoEmbed=discord.Embed(title="Created by PureCache#0001",color=discord.Color.orange())
        infoEmbed.set_author(name="Sentinel Information")
        infoEmbed.set_footer(text="Prefix: .s")

        for key in infoDict:
            infoEmbed.add_field(name=key,value=infoDict[key],inline=False)
        await ctx.send(embed=infoEmbed)
###########################################################################
    @commands.command(name='reload') #Reloads cogs
    @commands.has_permissions(administrator=True)
    async def reloadCogs(self, ctx, arg=None):
        
        with open("SentinelHelp.json","r") as cogFile:
            data=json.load(cogFile)
        data=data["Cogs"]
        cogList=list(data.keys())
        
        if not arg:
            await ctx.send("Please type either *.s reload all* to reload all cogs or *.s reload [cog]* to reload a certain cog")
            return await ctx.send(embed=discord.Embed(title='Cogs:', description="\n".join(cogList)))    
        if arg.lower() == 'all':
            for cog in cogList:
                cog=("Cogs."+cog)
                await ctx.send(f":arrows_counterclockwise: Reloading `{cog}`...")
                try:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                except:
                    await ctx.send(f":x: Reloading `{cog}` Failed!")
                else:
                    await ctx.send(f":white_check_mark: Reloaded `{cog}`")
        
        elif arg.lower() in cogList:
            cog=("Cogs."+arg.lower())
            await ctx.send(f":arrows_counterclockwise: Reloading `{cog}`...")
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except:
                await ctx.send(f":x: Reloading `{cog}` Failed!")
            else:
                await ctx.send(content=f":white_check_mark: Reloaded `{cog}`")
    @reloadCogs.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("Guess what noob? You don't have permission to do this!! :rofl: What a loser")
###########################################################################
def setup(bot):
    bot.add_cog(Misc(bot))
