import discord
import asyncio
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###########################################################################
    @commands.command(name="createrole", aliases=["addrole"])
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, name, colorCode=None):
        try:
            await ctx.send("Creating role... This may take a couple seconds...")
            guild=ctx.guild
            if colorCode:
                color=int("0x"+colorCode,0)
            else:
                color=int("0xffffff", 0)
            await guild.create_role(name=name,color=discord.Color(color))
            await ctx.send(":white_check_mark: Role successfully created")
        except Exception as e:
            await ctx.send("Invalid color-color! Example: 7289da (Do **NOT** include the #!)")
    
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
        await ctx.send("Role does not exist! Make sure to spell it correctly")

    @deleterole.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permissions to manage roles!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must supply a role to delete! Use *.s deleterole (role name)*")
###########################################################################
    @commands.command(name="giverole")
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
        if (ctx.author.top_role.position <= user.top_role.position) and (ctx.guild.owner.id != ctx.author.id):
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
    bot.add_cog(Roles(bot))
