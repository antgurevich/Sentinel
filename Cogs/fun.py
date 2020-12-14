import random
import time
import asyncio
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="fight")
    async def fight(self, ctx, user: discord.Member=None):
        
        await ctx.send("The shithead of an owner hasn't finished making this feature yet!! Check back later :slight_smile: ")
        return
        
        try:
            p1health=100
            p2health=100
            
            print (1)
            if user==ctx.author:
                await ctx.send("Uhhh... fighting with yourself? Just look in the mirror to do that")
                return
            print (2)
            duelMsg=await ctx.send(user.mention+", "+ctx.author.mention+" has challenged you to a duel! Choose a reaction to **attack**, **heal**, or **end**")
            
            emojiList=["⚔️","❤️","🏃‍♂️"]
            print (3)
            
            for reaction in reactionList:
                await duelMsg.add_reaction(emoji)
            def response():
                pass

            try:
                print (4)
                action=await self.bot.wait_for("reaction_add",check=response,timeout=10.0)
            except asyncio.TimeoutError:
                return await ("Bruh, you took too long to respond. Imagine forfeiting :stuck_out_tongue_closed_eyes:")
        
        except Exception as e:
            print (e)

    @fight.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MemberNotFound):
            await ctx.send("That person doesnt exist dumbass. Use *.s fight @[username]*")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("If you're gonna pick a fight with someone, at least actually pick a person :rolling_eyes: Use *.s fight @[username]*")
###########################################################################
    @commands.command(name="hack") #"Hacks" a tagged user or any phrase entered as argument
    async def hack(self,ctx, *, arg):
        msg=await ctx.send("Initiating "+arg+" hack")
        time.sleep(1)
        await msg.edit(content="Tracing IP address (0%)")
        await msg.edit(content="Tracing IP address (3%)")
        time.sleep(.5)
        await msg.edit(content="Tracing IP address (19%)")
        await msg.edit(content="Tracing IP address (30%)")
        await msg.edit(content="Tracing IP address (42%)")
        time.sleep(1)
        await msg.edit(content="Tracing IP address (56%)")
        time.sleep(2)
        await msg.edit(content="Tracing IP address (99%)")
        await msg.edit(content="**IP Trace Complete**\nIP: 506.457.14.512")
        time.sleep(1)
        await msg.edit(content="Accessing computer")
        time.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`smalldick69`")
        time.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`los3rhed`")
        time.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`n0fri3nds123`")
        time.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`plsMarryMeS0meOne`")
        await msg.edit(content="Calculating possible passwords:\n`hahaXDlolLMAO`")
        time.sleep(1)
        await msg.edit(content="Accessed computer: Password = `password`")
        await msg.edit(content="Downloading trojan virus...")
        time.sleep(1)
        await msg.edit(content="Virus downloaded. Extracting information")
        await msg.edit(content="Email: `mikeOxsmall@yahoo.com`")
        time.sleep(1)
        await msg.edit(content="Latest Email: `RE: Confirmation of Donation to Erectile Dysfunction Charity`")
        time.sleep(2)
        await msg.edit(content="Sending resignation letter to boss")
        time.sleep(1)
        await msg.edit(content="Discord: `v!rgin4ever#69420`")
        time.sleep(.5)
        await msg.edit(content="Current Discord Status: `:heart_eyes: Simping for someone out of my league`")
        time.sleep(1)
        await msg.edit(content="Keylogging bank PIN... [--Loading--]")
        time.sleep(.5)
        balance=("$"+str(random.randint(1,9))+str(random.randint(1,9))+"."+str(random.randint(1,9))+str(random.randint(1,9)))
        await msg.edit(content="Bank account retrieved\nCurrent Debit Card Balance: "+balance)
        time.sleep(1)
        await msg.edit(content="Tranferring balance to offshore account")
        time.sleep(.5)
        await msg.edit(content="Processing...")
        time.sleep(2)
        await msg.edit(content="Uninstalling Minecraft...")
        time.sleep(.5)
        await msg.edit(content="Switching default browser to Internet Explorer")
        time.sleep(.5)
        await msg.edit(content="Disabling adblocker")
        time.sleep(.5)
        await msg.edit(content="Medical records obtained")
        time.sleep(1)
        await msg.edit(content="Selling information to Russian government")
        time.sleep(1)
        await msg.edit(content="Hacking into school accounts...")
        time.sleep(.5)
        await msg.edit(content="Laughing at grades")
        time.sleep(1)
        await msg.edit(content="Sending dick pics to teachers...[1/13]")
        await msg.edit(content="Sending dick pics to teachers...[3/13]")
        await msg.edit(content="Sending dick pics to teachers...[7/13]")
        await msg.edit(content="Sending dick pics to teachers...[10/13]")
        time.sleep(.5)
        await msg.edit(content="**ERROR** TEACHER SENT ONE BACK :flushed:")
        time.sleep(1)
        await msg.edit(content="Can not compute... can not compute... Shutting down...")
        time.sleep(1)
        await msg.edit(content="*Initializing final completion procedures*")
        time.sleep(2)
        await msg.edit(content=(ctx.author.mention+", hack has been completed.\nComplete information here: <https://bit.ly/37cWufJ>"))
    
    @hack.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("We need a target!!! :face_with_symbols_over_mouth: Our team of hackers are waiting! Use .s hack [place or user]")
###########################################################################
    @commands.command(name="insult", aliases=["roast"]) #Chooses random insult from list to insult tagged user
    async def insult(self, ctx, user: discord.Member=None):
        insultList=[
                    "if laughter is the best medicine, your face must be curing the world"
                    ,"I guess you prove that even god makes mistakes sometimes"
                    ,"the only way you'll ever get laid is if you crawl up a chicken's ass and wait"
                    ,"if I wanted to kill myself I'd climb your ego and jump to your IQ"
                    ,"i'd slap you, but that would be animal abuse"
                    ,"keep rolling your eyes, perhaps you'll find a brain back there"
                    ,"you get ten times more girls than me? ten times zero is zero..."
                    ,"of course I talk like an idiot, how else would you understand me?"
                    ,"so, a thought crossed your mind? Must have been a long and lonely journey."
                    ,"you have two parts of brain, 'left' and 'right'. In the left side, there's nothing right. In the right side, there's nothing left"
                    ,"I'd like to see things from your point of view but I can't seem to get my head that far up my ass."
                    ,"I'm not insulting you. I'm describing you."
                    ,"you are proof that evolution CAN go in reverse."
                    ,"I would ask you how old you are but I know you can't count that high."
                    ,"if I had a face like yours, I'd sue my parents."
                    ,"Hell is wallpapered with all your deleted selfies."
                    ,"we all sprang from apes, but you didn't spring far enough."
                    ,"ordinarily people live and learn. You just live."
                    ,"your gene pool could use a little chlorine."
                    ,"which sexual position produces the ugliest children? Ask your mother."
                    ,"I don't know what makes you so stupid, but it really works."
                    ,"you're proof that god has a sense of humor."
                    ,"do you wanna lose ten pounds of ugly fat? Cut off your head."
                    ,"If what you don't know can't hurt you, you're invulnerable."
                    ]
        if user:
            await ctx.send("Hey "+user.mention+", "+random.choice(insultList))
        else:
            await ctx.send("Hey headass, are you trying to insult someone or what? Use *.s insult @[username]* , unless you want to keep doing it wrong :rolling_eyes:")

    @insult.error
    async def clear_error(self, ctx,error):
        if isinstance(error,commands.BadArgument):
            await ctx.send("Ping the user that you want to insult dipwad. Use *.s insult @[username]*")
###########################################################################
    @commands.command(name="compliment") #Chooses random compliment from list to compliment tagged user
    async def compliment(self, ctx, user: discord.Member=None):
        complimentList=[
                        "you're an awesome friend."
                        ,"you're a gift to those around you."
                        ,"you're a smart cookie."
                        ,"you are awesome!"
                        ,"you have impeccable manners."
                        ,"they like your style."
                        ,"you have the best laugh."
                        ,"they appreciate you."
                        ,"you are the most perfect you there is."
                        ,"you are enough."
                        ,"you're strong."
                        ,"your perspective is refreshing."
                        ,"they're grateful to know you."
                        ,"you light up the room."
                        ,"you deserve a hug right now."
                        ,"you should be proud of yourself."
                        ,"you're more helpful than you realize."
                        ,"you have a great sense of humor."
                        ,"you've got an awesome sense of humor!"
                        ,"you are really courageous."
                        ,"your kindness is a balm to all who encounter it."
                        ,"you're all that and a super-size bag of chips."
                        ,"on a scale from 1 to 10, you're an 11."
                        ,"you are strong."
                        ,"you're even more beautiful on the inside than you are on the outside."
                        ,"you have the courage of your convictions."
                        ,"they're inspired by you."
                        ,"you're like a ray of sunshine on a really dreary day."
                        ,"you are making a difference."
                        ,"they thank you for being there for them."
                        ,"you bring out the best in other people."
                        ]
        if user:
            await ctx.send(user.mention+", someone who's actually nice ("+ctx.author.mention+") wanted to tell you that "+random.choice(complimentList))
        else:
            await ctx.send("Yo dumbnuts, does the user you are trying to compliment even exist? Use .s compliment @[username]")
    @compliment.error
    async def clear_error(self, ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("You gotta actually ping the user you want to compliment... Use *.s compliment @[username]*")
###########################################################################
def setup(bot):
    bot.add_cog(Fun(bot))
