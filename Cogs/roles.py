import asyncio
import psycopg2
import os
from configparser import ConfigParser
import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###########################################################################
    @commands.command(name="exportroles", aliases=["exportrole","listroles","printroles"])
    async def exportroles(self, ctx): 
        channel=await ctx.author.create_dm() #Creates dm
        embed=discord.Embed(title=f"**{ctx.guild}** Role List:",color=discord.Color.teal())
        sum=0
        for role in ctx.guild.roles:
            amount=0
            sum+=1
            for user in ctx.guild.members:
                if role in user.roles:
                    amount+=1
            embed.add_field(name=role,value=f"{amount} users")
            if sum==30:
                await channel.send(embed=embed)
                embed=discord.Embed(title=f"**{ctx.guild}** Role List:",color=discord.Color.teal())
                sum=0
        await channel.send(embed=embed)
        await ctx.send(embed=discord.Embed(title="Roles dmed to you!"))
###########################################################################
    @commands.command(name="fetchrequests",aliases=["fetchreqs", "fetchreq", "fetchrequest"])
    async def fetchrequests(self, ctx):
        sql=("SELECT row_id, user_id, role_name, color FROM role_requests WHERE server_id=%s LIMIT 1;")
        cursor.execute(sql, (ctx.guild.id,))
        conn.commit()
        result=cursor.fetchone()
        if result is None:
            await ctx.send(embed=discord.Embed(title="No requests were found for this server!",color=discord.Color.red()))
            return
        embed=discord.Embed(title="Next Request:",color=discord.Color.gold())
        embed.add_field(name="ID",value=result[0])
        embed.add_field(name="User",value=f"<@{result[1]}>")
        embed.add_field(name="Role Name",value=result[2])
        embed.add_field(name="Color",value=result[3])
        await ctx.send(embed=embed)
###########################################################################
    @commands.command(name="exportreqs",aliases=["exportrequests"])
    @commands.has_permissions(manage_roles=True)
    async def exportreqs(self, ctx):
        sql=("SELECT row_id, user_id, role_name, color FROM role_requests WHERE server_id=%s;")
        cursor.execute(sql, (ctx.guild.id,))
        conn.commit()
        results=cursor.fetchall()
        if results is None: #No requests for the server
            await ctx.send(embed=discord.Embed(title="No requests were found for this server!",color=discord.Color.red()))
            return
        
        embed=discord.Embed(title="Role Request List",color=discord.Color.greyple())
        count=0
        for item in results:
            embed.add_field(name="ID",value=results[count][0])
            embed.add_field(name="User",value=(f"<@{results[count][1]}>"))
            embed.add_field(name="Role",value=results[count][2])
            embed.add_field(name="Color",value=results[count][3], inline=False)
            count+=1

        await ctx.send(embed=discord.Embed(title="Role Requests dmed to you!",color=discord.Color.green()))
        channel=await ctx.author.create_dm()
        await channel.send(embed=embed) #Sends dm with requests
    
    @exportreqs.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You do not have the proper permissions to do this!",color=discord.Color.red()))
###########################################################################
    @commands.command(name="rolerequest",aliases=["rolereq","requestrole","addreq","createreq"])
    #@commands.cooldown(1, 60, commands.BucketType.user)
    async def rolerequest(self, ctx, name, color=None):
        #Makes sure that user isn't submitting multiple requests for the same thing
        try:
            sql=('''SELECT * FROM role_requests WHERE (server_id=%s AND user_id=%s AND role_name=%s)''')
            cursor.execute(sql,(ctx.guild.id,ctx.message.author.id,name))
        except Exception as e:
            print (e)
        results=len(cursor.fetchall())
        if results>0:
            await ctx.send(embed=discord.Embed(title="You cannot submit multiple requests for the same role :/",color=discord.Color.orange()))
            return

        #Creates request in db
        sql=('''INSERT INTO role_requests(server_id, user_id, role_name, color)
            VALUES (%s, %s, %s, %s)''')
        if color is None: #Makes color value default to clear
            color="ffffff"
        cursor.execute(sql,(ctx.guild.id,ctx.message.author.id, name, color))
        conn.commit()
        await ctx.send(embed=discord.Embed(title="Request submitted! :slight_smile:",color=discord.Color.green()))
    
    @rolerequest.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You must supply a name for the role!",color=discord.Color.red()))
        elif isinstance(error,commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(title="You are currently on cooldown!"))
###########################################################################
    @commands.command(name="resolverequest",aliases=["resolvereq", "deleterequest", "removerequest","removereq", "delrequest"])
    @commands.has_permissions(manage_roles=True)
    async def resolverequest(self, ctx, role_id: int):
        try:
            sql=('''SELECT * FROM role_requests WHERE (server_id=%s AND row_id=%s)''')
            cursor.execute(sql, (ctx.guild.id, role_id))
            if cursor.fetchone() is None:
                await ctx.send(embed=discord.Embed(title="Role ID not found!"))
                return
            
            sql=('''DELETE FROM role_requests
                WHERE (server_id=%s AND row_id=%s)''')
            cursor.execute(sql, (ctx.guild.id,role_id))
            conn.commit()
            await ctx.send(embed=discord.Embed(title="Request Resolved :D",color=discord.Color.green()))
        except Exception as e:
            print(e)
    
    @resolverequest.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Must specify a role ID to delete!\nUse `.s exportreqs` and then `.s resolverequest (role_id)`",color=discord.Color.red()))
###########################################################################
    @commands.command(name="createrole")
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, name, colorCode=None):
        try:
            msg=await ctx.send(embed=discord.Embed(title="Creating role... This may take a couple seconds..."))
            guild=ctx.guild
            if colorCode:
                color=int("0x"+colorCode,0)
            else:
                color=int("0xffffff", 0)
            await guild.create_role(name=name,color=discord.Color(color))
            await ctx.send(embed=discord.Embed(title=":white_check_mark: Role successfully created",color=discord.Color.green()))
            msg.delete()
            
        except Exception as e:
            roleCount=0
            for role in ctx.guild.roles:
                roleCount+=1
            if roleCount==250:
                await ctx.send(embed=discord.Embed(title="Role limit (250) reached! Clear some space before trying to make a new one", color=discord.Color.red()))
            else:
                await ctx.send(embed=discord.Embed(title="Invalid color-color! Example: 7289da (Do NOT include the #!)",color=discord.Color.red()))
    
    @createrole.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You do not have permissions to manage roles!"))
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You did not provide proper arguments!Use `.s createrole (role name) [optional color-code]`\n**Use "" around the role name to add a multi-word role**"))
###########################################################################
    @commands.command(name="deleterole", aliases=["delrole"])
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, *, name):
        for role in ctx.guild.roles:
            if role.name.lower()==name.lower():
                await role.delete()
                await ctx.send(embed=discord.Embed(title=f"Role '{role}' deleted",color=discord.Color.green()))
                return
        await ctx.send(embed=discord.Embed(title="Role does not exist! Make sure to spell it correctly",color=discord.Color.red()))

    @deleterole.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You do not have permissions to manage roles!"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You must supply a role to delete! Use `.s deleterole (role name)`"))
###########################################################################
    @commands.command(name="giverole", aliases=["addrole"])
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, user: discord.Member, *, role: discord.Role):
        exceptions=[805830355290161153]#Smth
        if (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id) and (user.top_role.id not in exceptions):
            await ctx.send(embed=discord.Embed(title="You cannot give a role to someone with a higher role than you!"))
            return
        try:
            if role not in user.roles:
                await user.add_roles(role)
                await ctx.send(embed=discord.Embed(title=f"Role **{role}** given to {user}"))
            else:
                await ctx.send(embed=discord.Embed(title="This person already has this role!"))
        except Exception as e:
            print (e)

    @giverole.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="You do not have `Manage Roles` permissions!"))
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="User not found!"))
        elif isinstance(error,commands.RoleNotFound):
            await ctx.send(embed=discord.Embed(title="Role not found! Make sure to spell/capitalize it correctly"))
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing required argument! Use `.s giverole (user) (role name)`"))
###########################################################################
    @commands.command(name="removerole")
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, *, role: discord.Role):
        exceptions=[805830355290161153]#Smth
        if (ctx.author.top_role.position < user.top_role.position) and (ctx.guild.owner.id != ctx.author.id) and (user.top_role.id not in exceptions):
            await ctx.send(embed=discord.Embed(title="You cannot remove a role from someone with a higher role than you!"))
            return
        try:
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send(embed=discord.Embed(title=f"Role **{role}** removed from {user}"))
            else:
                await ctx.send(embed=discord.Embed(title="This person does not have this role!",color=discord.Color.red()))
        except Exception as e:
            print (e)

    @removerole.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Permissions `Manage Roles` is required for this!"))
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="User not found!"))
        elif isinstance(error,commands.RoleNotFound):
            await ctx.send(embed=discord.Embed(title="Role not found! Make sure to spell/capitalize it correctly"))
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing required argument! Use `.s removerole (user) (role name)`"))
###########################################################################
    @commands.command(name="editrole")
    @commands.has_permissions(manage_roles=True)
    async def editrole(self, ctx, *, role: discord.Role):
        ogAuthor=ctx.message.author
        msg = await ctx.send(embed=discord.Embed(title="Would you like to edit the name or color?"))
        reactions=["✏️","🌈"]
        for reaction in reactions:
            await msg.add_reaction(reaction)
        
        def check(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) in reactions)          

        def check2(user):
            return user != self.bot.user and ogAuthor == ctx.author

        try:
            response,_=await self.bot.wait_for("reaction_add",check=check, timeout=30)
            
            if response.emoji=="✏️":
                await ctx.send(embed=discord.Embed(title="Enter the name you would like to set it to"))
                response=await self.bot.wait_for("message",check=check2, timeout=30)
                await role.edit(name=response.content)
                await ctx.send(embed=discord.Embed(title=f"Role name changed to {role.name}", color=discord.Color.green()))

            else:
                await ctx.send(embed=discord.Embed(title="Enter the hexcode color you would like to set it to (i.e. 7289da)"))
                response=await self.bot.wait_for("message",check=check2, timeout=30)
                try:
                    color=int("0x"+str(response.content),0)
                    await role.edit(color=discord.Color(color))
                    await ctx.send(embed=discord.Embed(title="Role color changed", color=discord.Color(color)))
                except Exception as e:
                    await ctx.send(embed=discord.Embed(title="Invalid hex color-code. Example: 7289da",color=discord.Color.red()))
        except asyncio.TimeoutError:
            return await ctx.send(embed=discord.Embed(title="Connection timed out! Enter the original command to restart"))

    @editrole.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="`Manage Roles` permission is required for this command!"))
        elif isinstance(error,commands.RoleNotFound):
            await ctx.send(embed=discord.Embed(title="Role not found! Make sure to spell/capitalize it correctly"))
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Missing required argument! Use `.s editrole (role name)`"))
###########################################################################
def setup(bot):
    global cursor, conn
    try:
        conn=psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
        cursor = conn.cursor()
        print ("Roles Cog: Database connection established from environment")
    except:
        config_object=ConfigParser()
        config_object.read("SentinelVariables.ini")
        variables=config_object["variables"]
        DATABASE_URL=variables["DATABASE_URL"]
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        print ("Roles Cog: Database connection established from .ini")
    bot.add_cog(Roles(bot))
