import random
from configparser import ConfigParser
import os
import praw
import asyncio
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="meme", aliases=["reddit"])
    async def meme(self, ctx, sreddit=None, type=None):    
        try:
            CLIENT_ID=os.environ["CLIENT_ID"]
            CLIENT_SECRET=os.environ["CLIENT_SECRET"]
            USERNAME=os.environ["USERNAME"]
            PASSWORD=os.environ["PASSWORD"]
            USER_AGENT=os.environ["USER_AGENT"]
        except:
            config_object=ConfigParser()
            config_object.read("SentinelVariables.ini")
            variables=config_object["variables"]
            CLIENT_ID=variables["CLIENT_ID"]
            CLIENT_SECRET=variables["CLIENT_SECRET"]
            USERNAME=variables["USERNAME"]
            PASSWORD=variables["PASSWORD"]
            USER_AGENT=variables["USER_AGENT"]
        
        reddit=praw.Reddit(
                        client_id=CLIENT_ID
                        ,client_secret=CLIENT_SECRET
                        ,username=USERNAME
                        ,password=PASSWORD
                        ,user_agent=USER_AGENT)
        if sreddit==None:
            sreddit="memes"

        if type==None:
            subreddit=reddit.subreddit(sreddit).hot()
        elif type.lower()=="new":
            subreddit=reddit.subreddit(sreddit).new()
        elif type.lower()=="controversial":
            subreddit=reddit.subreddit(sreddit).controversial()
        else:
            await ctx.send("Incorrect post type. Must be either `hot`, `new`, or `controversial`")
            return

        post=random.randint(1,10)
        for i in range(0, post):
            submission=next(x for x in subreddit if not x.stickied)
        
        embed=discord.Embed(title=submission.title)
        embed.set_footer(text=("Posted by u/"+str(submission.author)))
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)
    
    @meme.error
    async def clear_error(self, ctx, error):
        await ctx.send("That subreddit does not exist! Make sure you spell it correctly")
###########################################################################
    @commands.command(name="cointoss", aliases=["flip", "coinflip", "coin"])
    async def cointoss(self, ctx):
        coin=["https://cdn.pixabay.com/photo/2013/07/12/19/19/coin-154560_640.png","https://th.bing.com/th/id/OIP.AhqNSM1dzobSLYaEIeQ68gHaHa?pid=Api&rs=1"] #[heads, tails]
        embed=discord.Embed(title="Flipping coin...")
        embed.set_image(url="https://media.giphy.com/media/10bv4HhibS9nZC/giphy.gif")
        await ctx.send(embed=embed)
        await asyncio.sleep(2)
        await ctx.message.channel.purge(limit=1)
        flip=random.choice(coin)
        if flip=="https://cdn.pixabay.com/photo/2013/07/12/19/19/coin-154560_640.png":
            title="It was heads!"
        else:
            title="It was tails!"
        embed=discord.Embed(title=title)
        embed.set_image(url=flip)
        await ctx.send(embed=embed)
###########################################################################
    @commands.command(name="8ball", aliases=["8-ball","eight ball", "eightball", "eight-ball", "8b"])
    async def eightBall(self, ctx, *, question=None):
        if question is None:
            await ctx.send("Uhh... are you going to ask a question?")
        elif "commit suicide" in question or "kill myself" in question or "off myself" in question or "go die" in question:
            await ctx.send("Dude. Please, no. :/\n<https://suicidepreventionlifeline.org/>")
        else:
            choices=["Hell yea!", "Duh...", "Lmaooooooo\nNo","Probably better not to tell you..."
                    ,"Of course not","Silly goose, not in a million years", "Pff never", "My sources say no"
                    ,"Of course my dude!", "Hell-freaking-yea!!","Maybe, who knows??", "Nah","Mmmmmm perhaps ^-^"
                    ,"Not even a question, of course!", "Go for it my guy!!", "hard to tell, ask again"]
            await ctx.send(random.choice(choices))
###########################################################################
    @commands.command(name="eatburger", aliases=["eat","munch","chomp"])
    async def eatburger(self, ctx):
        img=["https://viralviralvideos.com/wp-content/uploads/GIF/2014/09/Eating-hamburger-GIF.gif"
            ,"https://media1.tenor.com/images/db4d036795f662c70615b441193cbdff/tenor.gif?itemid=4131428"
            ,"https://cdn.firstwefeast.com/assets/2012/10/Ozersky.gif"
            ,"https://media.giphy.com/media/xT5LMxRvs78WoGa1G0/giphy.gif"
            ,"https://media.tenor.co/images/22956a7613064890b17d7ae7b5cb93c1/raw"
            ]
        author=str(ctx.message.author)[:-5]
        embed=discord.Embed(title=author+" when they go to McDonalds")
        embed.set_image(url=random.choice(img))
        await ctx.send(embed=embed)
###########################################################################
    @commands.command(name="kill", aliases=["murder"])
    async def kill(self, ctx, user: discord.Member=None):
        if user==ctx.message.author:
            await ctx.send(":flushed:... please don't")
        else:
            await ctx.send("No.")
###########################################################################
    @commands.command(name="hack") #"Hacks" a tagged user or any phrase entered as argument
    async def hack(self,ctx, *, arg):
        msg=await ctx.send("Initiating "+arg+" hack")
        await asyncio.sleep(1)
        await msg.edit(content="Tracing IP address (0%)")
        await msg.edit(content="Tracing IP address (3%)")
        await asyncio.sleep(.5)
        await msg.edit(content="Tracing IP address (19%)")
        await msg.edit(content="Tracing IP address (30%)")
        await msg.edit(content="Tracing IP address (42%)")
        await asyncio.sleep(1)
        await msg.edit(content="Tracing IP address (56%)")
        await asyncio.sleep(2)
        await msg.edit(content="Tracing IP address (99%)")
        await msg.edit(content="**IP Trace Complete**\nIP: 506.457.14.512")
        await asyncio.sleep(1)
        await msg.edit(content="Accessing computer")
        await asyncio.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`smalldick69`")
        await asyncio.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`los3rhed`")
        await asyncio.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`n0fri3nds123`")
        await asyncio.sleep(.5)
        await msg.edit(content="Calculating possible passwords:\n`plsMarryMeS0meOne`")
        await msg.edit(content="Calculating possible passwords:\n`hahaXDlolLMAO`")
        await asyncio.sleep(1)
        await msg.edit(content="Accessed computer: Password = `password`")
        await msg.edit(content="Downloading trojan virus...")
        await asyncio.sleep(1)
        await msg.edit(content="Virus downloaded. Extracting information")
        await msg.edit(content="Email: `mikeOxsmall@yahoo.com`")
        await asyncio.sleep(1)
        await msg.edit(content="Latest Email: `RE: Confirmation of Donation to Erectile Dysfunction Charity`")
        await asyncio.sleep(2)
        await msg.edit(content="Sending resignation letter to boss")
        await asyncio.sleep(1)
        await msg.edit(content="Discord: `v!rgin4ever#69420`")
        await asyncio.sleep(1)
        await msg.edit(content="Current Discord Status: `:heart_eyes: Simping for someone out of my league`")
        await asyncio.sleep(1)
        await msg.edit(content="Keylogging bank PIN... [--Loading--]")
        await asyncio.sleep(1)
        balance=("$"+str(random.randint(1,9))+str(random.randint(1,9))+"."+str(random.randint(1,9))+str(random.randint(1,9)))
        await msg.edit(content="Bank account retrieved\nCurrent Debit Card Balance: "+balance)
        await asyncio.sleep(1)
        await msg.edit(content="Tranferring balance to offshore account")
        await asyncio.sleep(.5)
        await msg.edit(content="Processing...")
        await asyncio.sleep(1)
        await msg.edit(content="Uninstalling Minecraft...")
        await asyncio.sleep(.5)
        await msg.edit(content="Switching default browser to Internet Explorer")
        await asyncio.sleep(.5)
        await msg.edit(content="Disabling adblocker")
        await asyncio.sleep(.5)
        await msg.edit(content="Medical records obtained")
        await asyncio.sleep(1)
        await msg.edit(content="Selling information to Russian government")
        await asyncio.sleep(1)
        await msg.edit(content="Hacking into school accounts...")
        await asyncio.sleep(.5)
        await msg.edit(content="Laughing at grades")
        await asyncio.sleep(1)
        await msg.edit(content="Sending dick pics to teachers...[1/13]")
        await msg.edit(content="Sending dick pics to teachers...[3/13]")
        await msg.edit(content="Sending dick pics to teachers...[7/13]")
        await msg.edit(content="Sending dick pics to teachers...[10/13]")
        await asyncio.sleep(.5)
        await msg.edit(content="**ERROR** TEACHER SENT ONE BACK :flushed:")
        await asyncio.sleep(1)
        await msg.edit(content="Can not compute... can not compute... Shutting down...")
        await asyncio.sleep(1)
        await msg.edit(content="*Initializing final completion procedures*")
        await asyncio.sleep(2)
        await msg.edit(content=(ctx.author.mention+", hack has been completed.\nComplete information here: <https://bit.ly/37cWufJ>"))
    
    @hack.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("We need a target!!! :face_with_symbols_over_mouth: Our team of hackers are waiting! Use .s hack [place or user]")
###########################################################################
    @commands.command(name="insult", aliases=["roast", "bully"]) #Chooses random insult from list to insult tagged user
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
                    ,"if what you don't know can't hurt you, you're invulnerable."
                    ,"whenever you join a group, you are the lowest common denominator."
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
