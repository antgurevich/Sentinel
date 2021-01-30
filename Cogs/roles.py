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
    @commands.command(name="fetchrequests",aliases=["fetchreqs", "fetchreq", "fetchrequest"])
    async def fetchrequests(self, ctx):
        
        await ctx.send(embed=discord.Embed(title="Currently disabled"))
        return
        
        sql=("SELECT user_id, role_name, color FROM role_requests WHERE server_id=%s LIMIT 1;")
        cursor.execute(sql, (ctx.guild.id,))
        conn.commit()
        result=cursor.fetchone()
        if result is None:
            await ctx.send(embed=discord.Embed(title="No requests were found for this server!",color=discord.Color.red()))
            return
        embed=discord.Embed(title="Next Request:",color=discord.Color.gold())
        embed.add_field(name="User",value=f"<@{result[0]}>")
        embed.add_field(name="Role Name",value=f"{result[1]}")
        embed.add_field(name="Color",value=f"{result[2]}")
        await ctx.send(embed=embed)
###########################################################################
    @commands.command(name="exportreqs",aliases=["exportrequests"])
    @commands.has_permissions(manage_roles=True)
    async def exportreqs(self, ctx):
        
        await ctx.send(embed=discord.Embed(title="Currently disabled"))
        return
        
        sql=("SELECT user_id, role_name, color FROM role_requests WHERE server_id=%s;")
        cursor.execute(sql, (ctx.guild.id,))
        conn.commit()
        results=cursor.fetchall()
        if results is None:
            await ctx.send(embed=discord.Embed(title="No requests were found for this server!",color=discord.Color.red()))
            return
        
        embed=discord.Embed(title="Role Request List",color=discord.Color.greyple())
        count=0
        for item in results:
            embed.add_field(name="User",value=(f"<@{results[count][0]}>"))
            embed.add_field(name="Role Name",value=results[count][1])
            embed.add_field(name="Color",value=results[count][2])
            count+=1

        await ctx.send(embed=discord.Embed(title="Role Requests dmed to you!",color=discord.Color.green()))
        channel=await ctx.author.create_dm()
        await channel.send(embed=embed)
    
    @exportreqs.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You do not have the proper permissions to do this!",color=discord.Color.red()))
###########################################################################
    @commands.command(name="rolerequest",aliases=["rolereq","requestrole","addreq","createreq"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rolerequest(self, ctx, name, colorCode=None):
        
        await ctx.send(embed=discord.Embed(title="Currently disabled"))
        return
        
        
        try:
            sql=('''SELECT * FROM role_requests WHERE (server_id=%s AND user_id=%s AND role_name=%s)''')
            cursor.execute(sql,(ctx.guild.id,ctx.message.author.id,name))
        except Exception as e:
            print (e)
        test=len(cursor.fetchall())
        print (test)
        if test>0:
            await ctx.send(embed=discord.Embed(title="You cannot submit multiple requests for the same role :/",color=discord.Color.orange()))
            return

        sql=('''INSERT INTO role_requests(server_id, user_id, role_name, color)
                VALUES (%s, %s, %s, %s)''')
        if colorCode is None:
            colorCode="ffffff"
        cursor.execute(sql,(ctx.guild.id,ctx.message.author.id, name, colorCode))
        conn.commit()
        await ctx.send(embed=discord.Embed(title="Request submitted! :slight_smile:",color=discord.Color.green()))
    
    @rolerequest.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="You must supply a name for the role!",color=discord.Color.red()))
        elif isinstance(error,commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(title="You are currently on cooldown!"))
###########################################################################
    @commands.command(name="resolverequest",aliases=["resolvereq"])
    @commands.has_permissions(manage_roles=True)
    async def resolverequest(self, ctx, user: discord.Member=None, role=None):
        
        await ctx.send(embed=discord.Embed(title="Currently disabled"))
        return
        
        if (user is not None and role is None) or (user is None and role is not None):
            await ctx.send(embed=discord.Embed(title="You must supply either both parameters or neither! Use `.s resolverequest [@user] [role name]`",color=discord.Color.red()))
            return
        elif user is None and role is None:
            try:
                sql=('''DELETE FROM role_requests
                    WHERE server_id=%s
                    LIMIT 1;''')
                cursor.execute(sql, (ctx.guild.id,))
                conn.commit()
                await ctx.send(embed=discord.Embed(title="Request Resolved :D",color=discord.Color.green()))
            except Exception as e:
                print(e)
        else:
            id=user.id
            if ctx.guild.get_member(id) is None:
                await ctx.send(embed=discord.Embed(title="This person is not in the server!",color=discord.Color.red()))
                return
            try:
                sql=('''DELETE FROM role_requests
                        WHERE (server_id=%s AND user_id=%s AND role_name=%s)
                        LIMIT 1''')
                cursor.execute(sql, (ctx.guild.id, id, role))
                conn.commit()
            except Exception as e:
                print (e)
            if cursor.rowcount==0:
                await ctx.send(embed=discord.Embed(title="No matching requests were found! Make sure to spell/capitalize the role name exactly as the requester did",color=discord.Color.red()))
            else:
                await ctx.send(embed=discord.Embed(title="Request Resolved :D",color=discord.Color.green()))
    
    @resolverequest.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.UserNotFound):
            await ctx.send(embed=discord.Embed(title="This person is not in the server!",color=discord.Color.red()))
###########################################################################
    @commands.command(name="deleterequest",aliases=["delrolereq","delrolerequest","deleterolerequest","removerequest","removereq","deleterequests","removerequests"])
    async def deleterequest(self, ctx, role=None):
        
        await ctx.send(embed=discord.Embed(title="Currently disabled"))
        return
        
        id=ctx.message.author.id 
        if role is None:
            sql=('''DELETE FROM role_requests
                    WHERE (server_id=%s AND user_id=%s);''')
            cursor.execute(sql,(ctx.guild.id, id))
            conn.commit()
            if cursor.rowcount==0:
                await ctx.send(embed=discord.Embed(title="No requests were found!",color=discord.Color.red()))
                return
        else:
            sql=('''DELETE FROM role_requests
                    WHERE (server_id=%s AND user_id=%s AND role_name=%s);''')
            cursor.execute(sql,(ctx.guild.id, id, role))
            conn.commit()
            if cursor.rowcount==0:
                await ctx.send(embed=discord.Embed(title="No role was found with that name! Did you spell/capitalize it correctly?",color=discord.Color.red()))
                return
        await ctx.send(embed=discord.Embed(title="Request(s) successfully deleted",color=discord.Color.green()))
###########################################################################
    @commands.command(name="createrole")
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, name, colorCode=None):
        try:
            msg=await ctx.send("Creating role... This may take a couple seconds...")
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
            await ctx.send("You do not have permissions to manage roles!")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("You did not provide proper arguments!Use *.s createrole (role name) [optional color-code]*\n**Use "" around the role name to add a multi-word role**")
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
            await ctx.send("You do not have permissions to manage roles!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must supply a role to delete! Use *.s deleterole (role name)*")
###########################################################################
    @commands.command(name="giverole", aliases=["addrole"])
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, user: discord.Member, *, role: discord.Role):
        if (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send("You cannot give a role to someone with a higher role than you!")
            return
        try:
            if role not in user.roles:
                await user.add_roles(role)
                await ctx.send(f"Role **{role}** given to {user.mention}")
            else:
                await ctx.send("This person already has this role!")
        except Exception as e:
            print (e)

    @giverole.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.send("User not found!")
        elif isinstance(error,commands.RoleNotFound):
            await ctx.send("Role not found! Make sure to spell/capitalize it correctly")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Missing required argument! Use *.s giverole (user) (role name)*")
###########################################################################
    @commands.command(name="removerole")
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, *, role: discord.Role):
        if (ctx.author.top_role.position < user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
            await ctx.send("You cannot remove a role from someone with a higher role than you!")
            return
        try:
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send(f"Role **{role}** removed from {user.mention}")
            else:
                await ctx.send("This person does not have this role!")
        except Exception as e:
            print (e)

    @removerole.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.send("User not found!")
        elif isinstance(error,commands.RoleNotFound):
            await ctx.send("Role not found! Make sure to spell/capitalize it correctly")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Missing required argument! Use *.s removerole (user) (role name)*")
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
            return await ctx.send("Connection timed out! Enter the original command to restart")

    @editrole.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.RoleNotFound):
            await ctx.send("Role not found! Make sure to spell/capitalize it correctly")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Missing required argument! Use *.s editrole (role name)*")
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
