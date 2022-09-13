import datetime
import discord
from discord.ext import commands, tasks

from Cogs.db import dbconnect

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clearYoinkTask.start()
###########################################################################
    @commands.command(name="forceleave",aliases=["botleave","guildleave","leaveguild"])
    @commands.is_owner()
    async def forceleave(self, ctx, id: int):
        try:
            guild=self.bot.get_guild(id)
            #guildList=list(self.bot.guilds)
            if guild in self.bot.guilds:#guildList:
                await guild.leave()
                await ctx.send(embed=discord.Embed(title="Left guild"))
            else:
                await ctx.send(embed=discord.Embed(title="Sentinel is not in this guild!"))
        except Exception as e:
            print(e)
###########################################################################
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        try:
            await ctx.send(embed=discord.Embed(title="Shutting down **Sentinel**..."))
            await self.bot.logout()
        except Exception as e:
            await ctx.send(embed=discord.Embed(title=f"Error occured: {e}"))
###########################################################################
    @commands.command(name="runsql", aliases=["runquery","sqlquery"])
    @commands.is_owner()
    async def runsql(self, ctx, *, sql):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            cursor.execute(sql)
            conn.commit()
            await ctx.send(embed=discord.Embed(title="Query Executed",color=discord.Color.green()))
            conn.close() #Closes connection to db
        except Exception as e:
            await ctx.send(embed=discord.Embed(title=f"Error occured: {e}"))
###########################################################################
    @commands.command(name="clearyoink")
    @commands.is_owner()
    async def clearyoink(self, ctx):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=("DELETE FROM yoink_command")
            cursor.execute(sql)
            conn.commit()
            await ctx.send(embed=discord.Embed(title="**yoink_command** table cleared"))
            conn.close() #Closes connection to db
        except Exception as e:
            await ctx.send(embed=discord.Embed(title=f"Error occured: {e}"))


    @tasks.loop(hours=12.0)
    async def clearYoinkTask(self):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=("DELETE FROM yoink_command")
            cursor.execute(sql)
            conn.commit()
            print (f"'yoink_commands' table cleared at {datetime.datetime.now()}")
            conn.close() #Closes connection to db
        except Exception as e:
            channel=self.bot.get_channel(784243375783149568)
            await channel.send(embed=discord.Embed(title=f"Error occured while clearing 'yoink_commands' table: {e}"))
###########################################################################
    @commands.command(name="shutdownmessage")
    @commands.is_owner()
    async def shutdownmessage(self, ctx):
        botguilds=list(self.bot.guilds)
        shutdown = "Hey everyone! Sentinel will be shutting down November 20th, 2022 due to the servers it is hosted on ending their free tier subscriptions. \nThere are currently no plans to continue hosting later on, but this might change.\nThank you for an amazing two years of support (:"
        #botguilds = [783840649282846731]
        print(botguilds)
        # for guild in botguilds:
        #     print(guild.id)
        for guild in botguilds:
            guild = self.bot.get_guild(guild.id)
            sysChannel=guild.system_channel
            if sysChannel:
                await sysChannel.send(embed = discord.Embed(title = 'Sentinel Shutdown', description = shutdown, color = discord.Color.blue()))

    
    @shutdownmessage.error
    async def clear_error(self, ctx, error):
        print(f"Error occured during sending message to all servers; Error: {error}")
###########################################################################
    @commands.command(name="sendmessage",aliases=["sendmsg","senddm","sendpm"])
    @commands.is_owner()
    async def sendmessage(self, ctx, id, *, message):
        user = self.bot.get_user(int(id))
        await user.send(message)
        await ctx.send(f"**Message sent to {user}:** {message}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None and not message.author.bot:
            user = self.bot.get_user(338707493188272129)
            await user.send(f"**{message.author} sent:** {message.content}")
            await self.bot.process_commands(message)
###########################################################################
    @commands.command(name="botservers",aliases=["botguilds","guildlist","serverlist"])
    @commands.is_owner()
    async def botservers(self, ctx):
        botguilds=list(self.bot.guilds)
        embed=discord.Embed(title="Guilds",color=discord.Color.magenta())
        for guild in botguilds:
            members=0
            for member in guild.members:
                members+=1
            embed.add_field(name=guild,value=members)#value=guild.channel[0].create_invite())
        await ctx.send(embed=embed)
###########################################################################
    @commands.command(name="blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx, id: int, type, reason=None):
        if type.lower()!="guild" and type.lower()!="user":
            await ctx.send(embed=discord.Embed("Parameter 'Type' must be either 'guild' or 'user'"))
            return 
        
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=("SELECT row_id FROM banned_entities WHERE (guild_id=%s OR user_id=%s);")
            cursor.execute(sql, (id,id))
            if cursor.fetchone() is not None: #Already blacklisted
                await ctx.send(embed=discord.Embed(title="User or guild is already blacklisted",color=discord.Color.red()))
                return
        except Exception as e:
            await ctx.send(f"Error: {e}")

        try:
            if type.lower()=="guild":
                sql=('''INSERT INTO banned_entities(guild_id, reason, ban_date)
                    VALUES (%s, %s, %s);''')
            else:
                sql=('''INSERT INTO banned_entities(user_id, reason, ban_date)
                    VALUES (%s, %s, %s);''')
            cursor.execute(sql, (id, reason, datetime.datetime.now()))
            conn.commit()
            await ctx.send(embed=discord.Embed(title="User or guild successfully blacklisted",color=discord.Color.green()))
        except Exception as e:
            await ctx.send(f"Error: {e}")
        conn.close() #Closes connection to db

    @blacklist.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Missing/incorrect parameter: `.s blacklist (id) (type) [reason]`"))
###########################################################################
    @commands.command(name="removeblacklist",aliases=["unbanguild"])
    @commands.is_owner()
    async def removeblacklist(self, ctx, id: int):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=("SELECT row_id FROM banned_entities WHERE (guild_id=%s OR user_id=%s);")
            cursor.execute(sql, (id, id))
            results=cursor.fetchone()
            if results is None: #Not blacklisted
                await ctx.send(embed=discord.Embed(title="This guild or user was not blacklisted!"))
                return
        except Exception as e:
            print (e)
        try:
            delsql=("DELETE FROM banned_entities WHERE (guild_id=%s OR user_id=%s);")
            cursor.execute(delsql, (id, id))
            conn.commit()
            await ctx.send(embed=discord.Embed(title="Guild/user removed from blacklist"))
        except Exception as e:
            print (e)
        conn.close() #Closes connection to db

    @removeblacklist.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument) or isinstance(error,commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Missing id (or not a number)"))
###########################################################################
    @commands.command(name='reload') #Reloads cogs
    @commands.is_owner()
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
###########################################################################
def setup(bot):
    bot.add_cog(Owner(bot))
