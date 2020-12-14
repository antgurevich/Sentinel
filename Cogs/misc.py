import datetime
import asyncio
import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="changelog",aliases=["changes","updates"])
    async def changelog(self,ctx):
        logEmbed=discord.Embed(title="Sentinel Change Log",color=discord.Color.teal())
        logDict={
                "12/13/20": "Added `changelog` command\nAdded role requirement for `reload` and `purge` commands"
                ,"12/12/20":"Initial version of Sentinel released"
                }
        for key in logDict:
            logEmbed.add_field(name=key,value=logDict[key],inline=False)
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
            await ctx.msg.delete()
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
        cogList = ["fun","misc"]
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