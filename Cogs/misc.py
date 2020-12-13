import datetime
import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="purge") #Clears previous x amount of messages (x between 1 & 50)
    async def purge(self, ctx, limit: int):
        if limit>50 or limit<1:
            await ctx.send("Oi cunt! I can only clear between 1 & 50 messages at a time, y u entering something outside that range?!?!")
            return
        try:
            await ctx.message.channel.purge(limit=limit)
        except discord.Forbidden:
            await ctx.send("You didn't give me enough permissions dipshit. Give me `Manage Messages` permission headass")
    
    @purge.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.BadArgument):
            await ctx.send("I can only delete a certain **number** of messages, not a certain **word** of messages, dipshit. Use *.s purge [x]*")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Bro, you gotta enter an amount of messages to clear. Use *.s purge [x]* , smh my head")
###########################################################################
    @commands.command(name="botinfo") #Displays informaton about Sentinel
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
###########################################################################
def setup(bot):
    bot.add_cog(Misc(bot))
