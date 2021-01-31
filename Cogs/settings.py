import os
from configparser import ConfigParser
import psycopg2
import discord
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###########################################################################
    @commands.command(name="setwelcomechannel")
    @commands.has_permissions(manage_guild=True)
    async def setwelcomechannel(self, ctx, channel: discord.TextChannel):
        channel=channel.id
        try:
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id, "welcome_channel"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                        SET setting_value=%s
                        WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, (channel, ctx.guild.id, "welcome_channel"))
                conn.commit()
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "welcome_channel",channel))
                conn.commit()
        except Exception as e:
            print (e)
        embed=discord.Embed(title="Join channel set!",color=discord.Color.green())
        await ctx.send(embed=embed)

    @setwelcomechannel.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Text channel not found!",color=discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Enter the text channel you want to set it to!\n`.s setwelcomechannel (channel)`",color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission",color=discord.Color.red()))
###########################################################################
    @commands.command(name="setleavechannel")
    @commands.has_permissions(manage_guild=True)
    async def setleavechannel(self, ctx, channel: discord.TextChannel):
        channel=channel.id
        try:
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id, "leave_channel"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                        SET setting_value=%s
                        WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, (channel, ctx.guild.id, "leave_channel"))
                conn.commit()
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "leave_channel",channel))
                conn.commit()
        except Exception as e:
            print (e)
        embed=discord.Embed(title="Leave channel set!",color=discord.Color.green())
        await ctx.send(embed=embed)
            
    @setleavechannel.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Text channel not found!",color=discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Enter the text channel you want to set it to!\n`.s setleavechannel (channel)`",color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission",color=discord.Color.red()))
###########################################################################
    @commands.command(name="setleavemsg")
    @commands.has_permissions(manage_guild=True)
    async def setleavemsg(self, ctx, *, message=None):
        if message is None:
            message=("Adios %s...")
        
        try:
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id,"leave_msg"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                    SET setting_value=%s
                    WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, (message, ctx.guild.id, "leave_msg"))
                conn.commit()
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "leave_msg",message))
                conn.commit()
            embed=discord.Embed(title="Leave message set!",color=discord.Color.green())
            embed.add_field(name="Test message:",value=message%ctx.author.mention)
            await ctx.send(embed=embed)
        except Exception as e:
            print (e)
        
    
    @setleavemsg.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission"))
###########################################################################
    @commands.command(name="enableleavemsg")
    @commands.has_permissions(manage_guild=True)
    async def enableleavemsg(self, ctx, status):
        if status.lower() not in ["true","false"]: #Incorrect status parameter
            await ctx.send(embed=discord.Embed(title="Incorrect parameters.\nMust be `.s enableleaveemsg (true/false)`"))
            return
        
        if status.lower()=="true":
            status="True"
            title="Leave message enabled"
        else:
            status="False"
            title="Leaver message disabled"
        sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
        cursor.execute(sql, (ctx.guild.id,"leave_status"))
        if cursor.fetchone() is not None:
            sql=('''UPDATE guild_settings
                SET setting_value=%s
                WHERE (guild_id=%s AND setting=%s)''')
            cursor.execute(sql, (status, ctx.guild.id, "leave_status"))
            conn.commit()
        else:
            sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                 VALUES (%s, %s, %s)''')
            cursor.execute(sql, (ctx.guild.id, "leavestatus",status))
            conn.commit()
        await ctx.send(embed=discord.Embed(title=title,color=discord.Color.dark_teal()))

    @enableleavemsg.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing required argument\nProper usage: `.s enableleavemsg (true/false)`"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission"))
###########################################################################
    @commands.command(name="leavepicture",aliases=["leavepic"])
    @commands.has_permissions(manage_guild=True)
    async def leavepicture(self, ctx, picture):
        if picture=="default":
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id,"leave_picture"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                    SET setting_value=%s
                    WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, ("https://media.giphy.com/media/ef0ZKzcEPOBhK/giphy.gif", ctx.guild.id, "leave_picture"))
                conn.commit()
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "leave_picture","https://media.giphy.com/media/ef0ZKzcEPOBhK/giphy.gif"))
                conn.commit()
            await ctx.send(embed=discord.Embed(title="Picture reset to default image"))
            return

        embed=discord.Embed(title="Test Image: Is this the correct image? React with the proper emoji")
        embed.set_image(url=picture)
        msg=await ctx.send(embed=embed)

        def check(reaction,user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) in reactEmojis)

        reactEmojis=["✔️","❌"]
        for emoji in reactEmojis:
            await msg.add_reaction(emoji)
        
        response,_=await self.bot.wait_for("reaction_add",check=check, timeout=30)
        if response.emoji=="✔️":
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id,"leave_picture"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                    SET setting_value=%s
                    WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, (picture, ctx.guild.id, "leave_picture"))
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "leave_picture",picture))
            conn.commit()
            await ctx.send(embed=discord.Embed(title="Leave picture set! :slight_smile:"))
        else:
            await ctx.send(embed=discord.Embed(title="Restart the command and try to paste a different link!"))

    @leavepicture.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing required argument. Use 'default' as the url to revert to original picture\nProper usage: `.s leavepicture (image link)`",color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission"))
###########################################################################
    @commands.command(name="setwelcomemsg")
    @commands.has_permissions(manage_guild=True)
    async def setwelcomemsg(self, ctx, *, message=None):
        if message is None:
            message=("Well well well... look who joined... welcome to hell %s")
        
        try:
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id,"welcome_msg"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                    SET setting_value=%s
                    WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, (message, ctx.guild.id, "welcome_msg"))
                conn.commit()
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "welcome_msg",message))
                conn.commit()
            embed=discord.Embed(title="Welcome message set!",color=discord.Color.green())
            embed.add_field(name="Test message:",value=message%ctx.author.mention)
            await ctx.send(embed=embed)
        except Exception as e:
            print (e)
    
    @setwelcomemsg.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission"))
###########################################################################
    @commands.command(name="enablewelcomemsg")
    @commands.has_permissions(manage_guild=True)
    async def enablewelcomemsg(self, ctx, status):
        if status.lower() not in ["true","false"]: #Incorrect status parameter
            await ctx.send(embed=discord.Embed(title="Incorrect parameters.\nMust be `.s enablewelcomemsg (true/false)`"))
            return
        
        if status.lower()=="true":
            status="True"
            title="Welcome message enabled"
        else:
            status="False"
            title="Welcome message disabled"
        sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
        cursor.execute(sql, (ctx.guild.id,"welcome_status"))
        if cursor.fetchone() is not None:
            sql=('''UPDATE guild_settings
                SET setting_value=%s
                WHERE (guild_id=%s AND setting=%s)''')
            cursor.execute(sql, (status, ctx.guild.id, "welcome_status"))
            conn.commit()
        else:
            sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                 VALUES (%s, %s, %s)''')
            cursor.execute(sql, (ctx.guild.id, "welcome_status",status))
            conn.commit()
        await ctx.send(embed=discord.Embed(title=title,color=discord.Color.dark_teal()))

    @enablewelcomemsg.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing required argument\nProper usage: `.s enablewelcomemsg (true/false)`"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission"))
###########################################################################
    @commands.command(name="welcomepicture",aliases=["welcomepic"])
    @commands.has_permissions(manage_guild=True)
    async def welcomepicture(self, ctx, picture):
        if picture=="default":
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id,"welcome_picture"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                    SET setting_value=%s
                    WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, ("https://media.tenor.co/images/3ccff8c4b2443d93811eac9b2fd56f11/raw", ctx.guild.id, "welcome_picture"))
                conn.commit()
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "welcome_picture","https://media.tenor.co/images/3ccff8c4b2443d93811eac9b2fd56f11/raw"))
                conn.commit()
            await ctx.send(embed=discord.Embed(title="Picture reset to default image"))
            return

        embed=discord.Embed(title="Test Image: Is this the correct image? React with the proper emoji")
        embed.set_image(url=picture)
        msg=await ctx.send(embed=embed)

        def check(reaction,user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) in reactEmojis)

        reacteEmojis=["✔️","❌"]
        for emoji in reactEmojis:
            await msg.add_reaction(emoji)
        
        response,_=await self.bot.wait_for("reaction_add",check=check, timeout=30)
        if response.emoji=="✔️":
            sql=("SELECT * FROM guild_settings WHERE (guild_id=%s AND setting=%s)")
            cursor.execute(sql, (ctx.guild.id,"welcome_picture"))
            if cursor.fetchone() is not None:
                sql=('''UPDATE guild_settings
                    SET setting_value=%s
                    WHERE (guild_id=%s AND setting=%s)''')
                cursor.execute(sql, (picture, ctx.guild.id, "welcome_picture"))
            else:
                sql=('''INSERT INTO guild_settings(guild_id, setting, setting_value)
                    VALUES (%s, %s, %s)''')
                cursor.execute(sql, (ctx.guild.id, "welcome_picture",picture))
            conn.commit()
            await ctx.send(embed=discord.Embed(title="Welcome picture set! :slight_smile:"))
        else:
            await ctx.send(embed=discord.Embed(title="Restart the command and try to paste a different link!"))

    @welcomepicture.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing required argument. Use 'default' as the url to revert to original picture\nProper usage: `.s welcomepicture (image link)`",color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Missing `Manage Server` permission"))
###########################################################################
def setup(bot):
    global cursor, conn
    try:
        conn=psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
        cursor = conn.cursor()
        print ("Settings Cog: Database connection established from environment")
    except:
        config_object=ConfigParser()
        config_object.read("SentinelVariables.ini")
        variables=config_object["variables"]
        DATABASE_URL=variables["DATABASE_URL"]
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        print ("Settings Cog: Database connection established from .ini")
    bot.add_cog(Settings(bot))