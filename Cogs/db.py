import asyncio
import psycopg2
import os
from configparser import ConfigParser
import discord
from discord.ext import commands

class db(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
def dbconnect():
    try:
        conn=psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
        cursor = conn.cursor()
    except:
        config_object=ConfigParser()
        config_object.read("SentinelVariables.ini")
        variables=config_object["variables"]
        DATABASE_URL=variables["DATABASE_URL"]
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
    return cursor, conn
###########################################################################
def setup(bot):
    bot.add_cog(db(bot))
