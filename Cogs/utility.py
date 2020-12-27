import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="temp", aliases=["convert","tempconvert","tconvert","tcon"])
    async def tempconvert(self, ctx, temp, unit):
        
        try:
            temp=int(temp)
        except:
            await ctx.send("Your temperature was not an integer! Use .s temp [temperature] [f or c]")
            return
        
        if unit.lower()!="f" and unit.lower()!="c":
            await ctx.send("You provided a wrong unit! Use .s temp [temperature] [f or c]")
            return
        
        if unit.lower()=="f":
            newTemp=((temp - 32) * 5.0/9.0)
            title=(str(temp)+"° Fahrenheit is "+str(newTemp)+"° Celsius")
            
        else:
            newTemp=((9.0/5.0 * temp) + 32)
            title=(str(temp)+"° Celsius is "+str(newTemp)+"° Fahrenheit")
        title=str(title)
        embed=discord.Embed(title=title, color=discord.Color.orange())

        await ctx.send(embed=embed)

    @tempconvert.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("You forgot a requirement! Use .s temp [temperature] [f or c]")
###########################################################################
def setup(bot):
    bot.add_cog(Utility(bot))
