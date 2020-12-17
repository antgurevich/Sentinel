import asyncio
import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member=None, *, reason=None):
        if user is None:
            await ctx.send("Who am I warning chief? You gotta tell me. Use *.s warn @username [optional_reason]*")
        elif (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send("You are trying to warn someone who has a role higher or equal to yours! Smh my head")
        else:
            #await ctx.message.channel.purge(limit=1)
            embed=discord.Embed(color=discord.Color.red())
            if reason:
                await user.send(f"You have been warned in **{ctx.guild}** for **{reason}**")
                #await ctx.send(f"You have been warned by {ctx.author.mention} for {reason}")
                embed.add_field(name="Warning", value=(f"**User **{user.mention} has been warned by {ctx.author.mention} for **{reason}**"))
            else:
                await user.send(f"You have been warned in **{ctx.guild}**")
                #await ctx.send(f"You have been warned by {ctx.author.mention} for {reason}")
                embed.add_field(name="Warning", value=(f"**User **{user.mention} has been warned by {ctx.author.mention}"))
            await ctx.send(embed=embed)
    @warn.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You can't warn people smallbrain, you don't have permission.")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("You did it wrong... Do *.s warn @username [optional_reason]")
###########################################################################
    @commands.command(name="mute")
    @commands.has_permissions(kick_members=True)
    async def mute(self,ctx, user: discord.Member=None, time: str = None):
        if user is None:
            await ctx.send("Dude I need a username to be able to mute them :rolling_eyes: Use *.s mute @username [time]* Example: *.s mute @username 5m*")
        elif (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send("You are trying to mute someone who has a role higher or equal to yours! Smh my head")
        else:
            guild=ctx.guild
            muteRole=None

            for role in guild.roles: #Checks to see if Muted role exists
                if role.name.lower()=="muted":
                    muteRole=role
                    break
            if muteRole in user.roles: #If user is already muted
                await ctx.send("Lmao they're already muted")
            else:
                if not muteRole: #If muted role doesn't exist, creates one
                    await ctx.send("This server doesn't have the `Muted` role set up, lemme do it for you right now")
                    await ctx.send("This might take a little just be patient")
                    
                    perms=discord.Permissions(send_messages=False)
                    muteRole=await guild.create_role(name="Muted",color=discord.Color.dark_grey(),permissions=perms)
                    for channel in guild.channels:
                        await channel.set_permissions(muteRole,send_messages=False)
                 
                if time is None: #Permamuted
                    await user.add_roles(muteRole)
                    await ctx.send(f"User {user.mention} got muted, what an L")
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
                    await ctx.send(f"User {user.mention} has been silenced for {parsedTime} {timeUnit}!")

                    if timeUnit == "seconds":
                        await asyncio.sleep(int(parsedTime))
                    elif timeUnit == "minute(s)":
                        await asyncio.sleep(int(parsedTime) * 60)
                    elif timeUnit == "hour(s)":
                        await asyncio.sleep(int(parsedTime) * 3600)
            
                    await user.remove_roles(muteRole)
                    await ctx.send(f"User {user.mention} has been unmuted after {parsedTime} {timeUnit}!")

    @mute.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You can't mute people dipshit, you don't have permission.")
###########################################################################
    @commands.command(name="unmute")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user:discord.Member=None):
        if user is None:
            await ctx.send("Who am I unmuting? You gotta tell me who, use *.s unmute @username*")
        elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
            await ctx.send("Can't unmute someone who has the same or higher role than yours!!")
        else:
            guild = ctx.guild
            muteRole = None

            for role in guild.roles:
                if role.name.lower() == "muted":
                    muteRole = role
                    break

            if muteRole in user.roles:
                await user.remove_roles(muteRole)
                await ctx.send(f"User {user.mention} has been unmuted! Now we have to listen to their shit again...")

            else:
                await ctx.send("This user was never muted.")
    @unmute.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You can't unmute people dipshit, you don't have permission.")
###########################################################################
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, user: discord.Member=None, *, reason=None):
        if user is None:
            await ctx.send("Buddy, you gotta tell me who to kick :rolling_eyes: Use *.s kick @username [reason]*")
        elif (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send("You are trying to kick someone who has a role higher or equal to yours! Smh my head")
        else:
            await ctx.guild.kick(user, reason=reason)
            if reason:
                await ctx.send(str(user)+" has been yeeted from the server for "+str(reason))
                await user.send("Yikes, you just got kicked from **"+str(ctx.guild)+"**. Reason: "+str(reason))
            else:
                await ctx.send(str(user)+" has been yeeted from the server.")
                await user.send("You have been kicked from **"+str(ctx.guild)+"**. No reason was given. LLLL")
    @kick.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("HA LOOK AT THIS LOSER, doesn't even have permission to kick people. Imagine not being a mod, yikes")
###########################################################################
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, user: discord.Member=None, *, reason=None):
        if user is None:
            await ctx.send("Buddy, you gotta tell me who to ban :rolling_eyes: Use *.s ban @username [reason]*")
        elif (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send("You are trying to ban someone who has a role higher or equal to yours! Smh my head")
        else:
            await ctx.guild.ban(user, reason=reason)
            if reason:
                await ctx.send(str(user)+" has been **permanently** yeeted from the server for "+str(reason))
                await user.send("Yikes, you just got banned from **"+str(ctx.guild)+"**. Reason: "+str(reason))
            else:
                await ctx.send(str(user)+" has been **permanently** yeeted from the server.")
                await user.send("You have been banned from **"+str(ctx.guild)+"**. No reason was given. LLLL")
    @ban.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("HA LOOK AT THIS LOSER, doesn't even have permission to ban people. Imagine not being a mod, yikes")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("You have to tag the user you want to ban. Use *.s ban @username [reason]* you shmuck")
###########################################################################
    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, username: str = None, *, reason=None):
        if username is None:
            await ctx.send("Gotta supply a person to unban, genius. Use *.s unban username#tags*")

        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = username.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    print ("test")

            try:
                await ctx.send(f"Fine, I suppose {user} can come back :rolling_eyes:")
                await user.send(f"You have been **unbanned** from **{ctx.guild}** server")
            except NameError:
                await ctx.send(f"{username} isn't even banned... you sure you spelled it right?")
    
    @unban.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("If you don't have perms to ban people... why would you think you can unban them?")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("You did it wrong 4head, use *.s unban username#tags*")
###########################################################################
def setup(bot):
    bot.add_cog(Mod(bot))
