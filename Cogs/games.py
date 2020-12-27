import asyncio
import random
import discord
from discord.ext import commands

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="fight")
    async def fight(self, ctx, p2: discord.Member=None):
        
        await ctx.send("The shithead of an owner hasn't finished making this feature yet!! Check back later :slight_smile: ")
        return
        
        try:
            p1health=100
            p2health=100
            p1=ctx.author
            print (1)
            if p2==ctx.author:
                await ctx.send("Uhhh... fighting with yourself? Just look in the mirror to do that")
                return
            print (2)
            duelMsg=await ctx.send(p2.mention+", "+ctx.author.mention+" has challenged you to a duel! Choose a reaction to **attack**, **heal**, or **end**")
            
            fightEmojiList=["⚔️","❤️","🏃‍♂️"]
            print (3)
            
            for emoji in fightEmojiList:
                await duelMsg.add_reaction(emoji)
            
            def check(reaction, player):
                print (reaction, player)
                if player!=self.bot.user: #and reaction=="🏃‍♂️":
                     #await ctx.send(player.mention+" pussied out! "+p1.mention+" wins the duel!")
                     print (player.mention+" pussied out! "+p1.mention+" wins the duel!")
                else:
                    print (False)

            try:
                print (4)
                response,_=await self.bot.wait_for("reaction_add",check=check,timeout=60.0)
                
            except asyncio.TimeoutError:
                return await ctx.send("Bruh, you took too long to respond. Imagine forfeiting :stuck_out_tongue_closed_eyes:")
        
        except Exception as e:
            print (e)

    @fight.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MemberNotFound):
            await ctx.send("That person doesnt exist dumbass. Use *.s fight @[username]*")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("If you're gonna pick a fight with someone, at least actually pick a person :rolling_eyes: Use *.s fight @[username]*")
###########################################################################
    @commands.command(name="rps", aliases=["rockpaperscissors"])
    async def rps(self, ctx):
        rpsEmojis=["🌑", "📄", "✂"]
        
        embed=discord.Embed(title=("So... you want to challenge me to rock paper scissors, huh?\nReact to this message with your choice"))
        botMsg = await ctx.send(embed=embed)
        
        for emoji in rpsEmojis:
            await botMsg.add_reaction(emoji)
        
        bChoice=random.choice(rpsEmojis)
        #await ctx.send(bChoice)
        
        def rpsaction(reaction,user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) in rpsEmojis) #'🌑' or '📄' or '✂')            
        
        try:
            response,_ =await self.bot.wait_for("reaction_add",check=rpsaction,timeout=30)
            if response.emoji==bChoice:
                resultsMsg=("We tied! You got super lucky...:expressionless:")
            elif response.emoji=="🌑":
                if bChoice=="📄":
                    resultsMsg=("LLLLL I chose paper, imagine losing :rofl:")
                else:
                    resultsMsg=("Oh... I chose scissors :fearful: You win I guess")
            elif response.emoji=="📄":
                if bChoice=="🌑":
                    resultsMsg=("Oh... I chose rock :fearful: You win I guess")
                else:
                    resultsMsg=("LLLLL I chose scissors, imagine losing :rofl:")
            else: #User chose scissors
                if bChoice=="🌑":
                    resultsMsg=("LLLLL I chose rock, imagine losing :rofl:")
                else:
                    resultsMsg=("Oh... I chose paper :fearful: You win I guess")
            embed=discord.Embed(title=resultsMsg)
            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            return await ctx.send("Thanks for taking so long, dipshit. I'm taking this as a win for me LLL")
###########################################################################
def setup(bot):
    bot.add_cog(Games(bot))
