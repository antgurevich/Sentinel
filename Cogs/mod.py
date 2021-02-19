import asyncio
import psycopg2
import os
from configparser import ConfigParser
import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="slowmode", aliases=["smode"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int=None):
        if time==0 or time is None: #Disabled slowmode
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(embed=discord.Embed(title="Slowmode disabled"))
        elif time<0 or time>21599: #Out of range
            await ctx.send(embed=discord.Embed(title="You cannot set a time lower than 0 seconds or greater than 21599 seconds! 0 seconds disables slowmode"))
        else: #Correct range
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send(embed=discord.Embed(title=f"Slowmode set to {time} seconds"))
    
    @slowmode.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="HA you don't have the proper perms to do that. What an L"))
        elif isinstance(error,commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="You must enter an integer: `.s slowmode (seconds)`"))
###########################################################################
    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        perms=ctx.channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages=False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        await ctx.send(embed=discord.Embed(title=f"**{ctx.channel}** locked to non-admin users"))
    
    @lock.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You don't have perms to do that dummy"))
###########################################################################
    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        perms=ctx.channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages=True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        await ctx.send(embed=discord.Embed(title=f"**{ctx.channel}** unlocked to non-admin users"))
    
    @unlock.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You don't have perms to do that dummy"))
###########################################################################
    @commands.command(name="warnlist",aliases=["listwarns"])
    @commands.has_permissions(kick_members=True)
    async def warnlist(self, ctx, user: discord.Member):
        try:
            sql=('''SELECT row_id, reason FROM warning_history WHERE (guild_id=%s AND user_id=%s);''')
            cursor.execute(sql, (ctx.guild.id, user.id))
            results=cursor.fetchall()
        except Exception as e:
            print (e)
        if len(results)==0:
            await ctx.send(embed=discord.Embed(title="This user has no history of warns!"))
            return
        embed=discord.Embed(title=f"{user}'s Warning History:",color=discord.Color.dark_blue())
        x=0
        for warn in results:
            embed.add_field(name=f"{x+1})  Warn ID: {results[x][0]}",value=f"Reason: {results[x][1]}")
            x+=1
        await ctx.send(embed=embed)

    @warnlist.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You do not have the `Kick Members` permission!"))
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="Could not find this user! Make sure to ping them correctly"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Incorrect argument type! Use `.s warnlist (@user)`"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Enter the person you want to list the warns of! Use `.s warnlist (@user)`"))
###########################################################################
    @commands.command(name="unwarn", aliases=["clearwarn","delwarn","removewarn","deletewarn"])
    @commands.has_permissions(kick_members=True)
    async def unwarn(self, ctx, user: discord.Member, id: int):
        try:
            sql=('''SELECT * FROM warning_history WHERE (guild_id=%s AND user_id=%s AND row_id=%s);''')
            cursor.execute(sql, (ctx.guild.id, user.id,id))
            results=cursor.fetchone()
            if results is None:
                await ctx.send(embed=discord.Embed(title="Warning ID not found! Use `.s warnlist (@user)` to select the right ID!"))
                return
                
            sql=('''DELETE FROM warning_history WHERE (guild_id=%s AND user_id=%s AND row_id=%s);''')
            cursor.execute(sql, (ctx.guild.id, user.id,id))
            conn.commit
           
        except Exception as e:
            print (e)
        await ctx.send(embed=discord.Embed(title="Warning successfully deleted!"))

    @unwarn.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You do not have the `Kick Members` permission!"))
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="Could not find this user! Make sure to ping them correctly"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Incorrect argument type! Use `.s unwarn (@user) (warn ID)`"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Enter the person you want to unwarn & warning ID!\nUse `.s warnlist (@user)` to find the IDs, and then `.s unwarn (@user) (warn ID)`"))
###########################################################################
    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason=None):
        exceptions=[805830355290161153]#Smth
        if (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id) and (user.top_role.id not in exceptions):
            await ctx.send(embed=discord.Embed(title="You are trying to warn someone who has a role higher or equal to yours! Smh my head"))
        else:
            embed=discord.Embed(color=discord.Color.red())
            if reason:
                await user.send(embed=discord.Embed(title=f"You have been warned in **{ctx.guild}** for **{reason}**"))
                embed.add_field(name="Warning", value=(f"**User **{user.mention} has been warned by {ctx.author.mention} for **{reason}**"))
            else:
                await user.send(embed=discord.Embed(title=f"You have been warned in **{ctx.guild}**"))
                embed.add_field(name="Warning", value=(f"**User **{user.mention} has been warned by {ctx.author.mention}"))
            sql=('''INSERT INTO warning_history(guild_id, user_id, reason)
                    VALUES (%s, %s, %s)''')
            cursor.execute(sql, (ctx.guild.id,user.id, reason))
            conn.commit()
            await ctx.send(embed=embed)
    
    @warn.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You can't warn people smallbrain, you don't have permission."))
        elif isinstance(error,commands.BadArgument) or isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="You did it wrong... Do `.s warn (@username) [optional_reason]`"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Dude I need a username to be able to mute them :rolling_eyes: Use `.s mute (@username) [time]` Example: `.s mute @username 5m`"))
###########################################################################
    @commands.command(name="mute")
    @commands.has_permissions(kick_members=True)
    async def mute(self,ctx, user: discord.Member, time: str = None, *, reason):
        exceptions=[805830355290161153]#Smth
        if (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id) and (user.top_role.id not in exceptions):
            await ctx.send(embed=discord.Embed(title="You are trying to mute someone who has a role higher or equal to yours! Smh my head",color=discord.Color.red()))
        else:
            guild=ctx.guild
            muteRole=None

            for role in guild.roles: #Checks to see if Muted role exists
                if role.name.lower()=="muted":
                    muteRole=role
                    break
            if muteRole in user.roles: #If user is already muted
                await ctx.send(embed=discord.Embed(title="Lmao they're already muted"))
            else:
                if not muteRole: #If muted role doesn't exist, creates one
                    await ctx.send(embed=discord.Embed(title="This server doesn't have the `Muted` role set up, lemme do it for you right now\nThis might take a little, please be patient"))
                    
                    perms=discord.Permissions(send_messages=False)
                    muteRole=await guild.create_role(name="Muted",color=discord.Color.dark_grey(),permissions=perms)
                    for channel in guild.channels:
                        await channel.set_permissions(muteRole,send_messages=False)
                 
                if time is None: #Permamuted
                    await user.add_roles(muteRole)
                    embed=discord.Embed()
                    embed.add_field(name="You guys wanna see a joke?",value=f"{user.mention} getting muted for *{reason}*")
                    await ctx.send(embed=embed)
                
                else: #User specified time limit
                    timeUnit=None
                    parsedTime=None
                    if "s" in time:
                        timeUnit="seconds"
                        parsedTime=time[0:(len(time)-1)]
                    elif "m" in time:
                        timeUnit="minute(s)"
                        parsedTime=time[0:(len(time)-1)]
                    elif "h" in time:
                        timeUnit="hour(s)"
                        parsedTime=time[0:(len(time)-1)]
                    else: #Defaults to minutes if user doesn't provide time unit
                        timeUnit="minute(s)"
                        parsedTime=time[0:(len(time)-1)]

                    await user.add_roles(muteRole)
                    embed=discord.Embed()
                    
                    embed.add_field(name="You guys wanna see a joke?",value=f"{user.mention} getting silenced for {parsedTime} {timeUnit} for *{reason}*, what an L")
                    
                    await ctx.send(embed=embed)

                    if timeUnit == "seconds":
                        await asyncio.sleep(int(parsedTime))
                    elif timeUnit == "minute(s)":
                        await asyncio.sleep(int(parsedTime) * 60)
                    elif timeUnit == "hour(s)":
                        await asyncio.sleep(int(parsedTime) * 3600)
                    
                    if muteRole in user.roles:
                        await user.remove_roles(muteRole)
                        await ctx.send(embed=discord.Embed(title=f"{user} has been unmuted after {parsedTime} {timeUnit}!",color=discord.Color.red()))

    @mute.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You can't mute people dipshit, you don't have permission"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You missed a parameter :rolling_eyes:\nUse `.s mute (@username) [time] (reason)`\nExample: `.s mute @test_user 5m spam`"))
        elif isinstance(error, commands.BadArgument) or isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="Invalid user! Use `.s mute (@username) [time] (reason)`"))
###########################################################################
    @commands.command(name="unmute")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        exceptions=[805830355290161153]#Smth
        if ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id and user.top_role.id not in exceptions:
            await ctx.send(embed=discord.Embed(title="Can't unmute someone who has the same or higher role than yours!!"))
        else:
            guild = ctx.guild
            muteRole = None

            for role in guild.roles:
                if role.name.lower() == "muted":
                    muteRole = role
                    break

            if muteRole in user.roles:
                await user.remove_roles(muteRole)
                await ctx.send(embed=discord.Embed(title=f"{user} has been unmuted! Now we have to listen to their shit again..."))
            else:
                await ctx.send("This user was never muted.")
    
    @unmute.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You can't unmute people dipshit, you don't have permission."))
        elif isinstance(error, commands.BadArgument) or isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="Invalid user! Use `.s unmute (@username)`"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Who am I unmuting? You gotta tell me who, use `.s unmute @username`"))

###########################################################################
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, user: discord.Member, *, reason=None):
        if (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send(embed=discord.Embed(title="You are trying to kick someone who has a role higher or equal to yours! Smh my head"))
        else:
            await ctx.guild.kick(user, reason=reason)
            if reason:
                await ctx.send(embed=discord.Embed(title=f"{user} has been yeeted from the server for {reason}"))
                await user.send(embed=discord.Emed(title=f"Yikes, you just got kicked from **{ctx.guild}**. Reason: {reason}"))
            else:
                await ctx.send(embed=discord.Embed(title=f"{user} has been yeeted from the server."))
                await user.send(embed=discord.Embed(title=f"You have been kicked from **{ctx.guild}**. No reason was given. LLLL"))
    
    @kick.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="HA LOOK AT THIS LOSER, doesn't even have permission to kick people. Imagine not being a mod, yikes"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You didn't specify who to kick... use `.s kick (@user) [reason]`"))
        elif isinstance(error, commands.BadArgument) or isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="Could not find this user... did you ping them correctly?"))
###########################################################################
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, user: discord.Member, *, reason=None):
        exceptions=[805830355290161153]#Smth
        if (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id) and (user.top_role.id not in exceptions):
            await ctx.send(embed=discord.Embed(title="You are trying to ban someone who has a role higher or equal to yours! Smh my head"))
        else:
            await ctx.guild.ban(user, reason=reason)
            if reason:
                await ctx.send(embed=discord.Embed(title=f"{user} has been **permanently** yeeted from the server for {reason}"))
                await user.send(embed=discord.Embed(title=f"Yikes, you just got banned from **{ctx.guild}**. Reason: {reason}"))
            else:
                await ctx.send(embed=discord.Embed(title=f"{user} has been **permanently** yeeted from the server"))
                await user.send(embed=discord.Embed(title=f"You have been banned from **{ctx.guild}**. No reason was given. LLLL"))
    
    @ban.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="HA LOOK AT THIS LOSER, doesn't even have permission to ban people. Imagine not being a mod, yikes"))
        elif isinstance(error,commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You have to tag the user you want to ban. Use `.s ban @username [reason]` you shmuck"))
###########################################################################
    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, username: str, *, reason=None):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = username.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

        try:
            await ctx.send(embed=discord.Embed(title=f"Fine, I suppose {user} can come back :rolling_eyes:"))
            await user.send(embed=discord.Embed(title=f"You have been **unbanned** from **{ctx.guild}** server"))
        except NameError:
            await ctx.send(embed=discord.Embed(title=f"{username} isn't even banned... you sure you spelled it right?"))
    
    @unban.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="If you don't have perms to ban people... why would you think you can unban them?"))
        elif isinstance(error,commands.BadArgument) or isinstance(error, commands.UserNotFound) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You did it wrong 4head, use `.s unban username#tags`"))
###########################################################################
def setup(bot):
    global cursor, conn
    try:
        conn=psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
        cursor = conn.cursor()
        print ("Mod Cog: Database connection established from environment")
    except:
        config_object=ConfigParser()
        config_object.read("SentinelVariables.ini")
        variables=config_object["variables"]
        DATABASE_URL=variables["DATABASE_URL"]
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        print ("Mod Cog: Database connection established from .ini")
    bot.add_cog(Mod(bot))
