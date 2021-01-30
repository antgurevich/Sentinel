import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###########################################################################
    @commands.command(name="sendmessage",aliases=["sendmsg","senddm","sendpm"])
    @commands.is_owner()
    async def sendmessage(self, ctx, id, *, message):
        user = self.bot.get_user(int(id))
        await user.send(message)
        await ctx.send(f"Message sent to {user}: {message}")

    @sendmessage.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.NotOwner):
            await ctx.send("You're not the owner dummy")
    '''
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None and not message.author.bot:
            user = self.bot.get_user(338707493188272129)
            await user.send(f"**{message.author} sent:** {message.content}")
        await self.bot.process_commands(message)'''
###########################################################################
def setup(bot):
    bot.add_cog(Owner(bot))
