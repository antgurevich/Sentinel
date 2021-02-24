import datetime
import discord
from discord.ext import commands, tasks

from Cogs.db import dbconnect

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clearYoinkTask.start()
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
    @commands.command(name="blacklist",aliases=["banguild","guildban"])
    @commands.is_owner()
    async def blacklist(self, ctx, guildID, reason=None):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=("SELECT * FROM banned_guilds WHERE guild_id=%s;")
            cursor.execute(sql, (guildID,))
            if cursor.fetchone() is not None: #Guild already blacklisted
                await ctx.send(embed=discord.Embed(title="Guild is already blacklisted",color=discord.Color.red()))
                return
        except Exception as e:
            print (e)
        try:
            sql=('''INSERT INTO banned_guilds(guild_id, reason, ban_date)
                VALUES (%s, %s, %s);''')
            cursor.execute(sql, (guildID, reason, datetime.datetime.now()))
            conn.commit()
            await ctx.send(embed=discord.Embed(title="Guild successfully blacklisted",color=discord.Color.green()))
        except Exception as e:
            print (e)
        conn.close() #Closes connection to db

    @blacklist.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing guildID"))
###########################################################################
    @commands.command(name="removeblacklist",aliases=["unbanguild"])
    @commands.is_owner()
    async def removeblacklist(self, ctx, guildID: int):
        cursor,conn=dbconnect() #Opens connection to db
        try:
            sql=("SELECT guild_id FROM banned_guilds WHERE guild_id=%s;")
            cursor.execute(sql, (guildID,))
            results=cursor.fetchone()
            if results is None: #Guild is not blacklisted
                await ctx.send(embed=discord.Embed(title="This guild was not blacklisted!"))
                return
        except Exception as e:
            print (e)
        try:
            delsql=("DELETE FROM banned_guilds WHERE guild_id=%s;")
            cursor.execute(delsql, (guildID,))
            conn.commit()
            await ctx.send(embed=discord.Embed(title="Guild removed from blacklist"))
        except Exception as e:
            print (e)
        conn.close() #Closes connection to db

    @removeblacklist.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing guildID"))
###########################################################################
def setup(bot):
    bot.add_cog(Owner(bot))
