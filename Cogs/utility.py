import requests
import json
from covid import Covid
from configparser import ConfigParser
import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
###########################################################################
    @commands.command(name="covid", aliases=["corona","covid19","covid-19"])
    async def covid(self, ctx, country=None):
        covid=Covid(source="worldometers")
        if country==None:
            active=covid.get_total_active_cases()
            confirmed = covid.get_total_confirmed_cases()
            recovered = covid.get_total_recovered()
            deaths = covid.get_total_deaths()
            
            embed=discord.Embed(title="Global COVID-19 Statistics")
            embed.add_field(name="Active",value=active)
            embed.add_field(name="Total Confirmed",value=confirmed)
            embed.add_field(name="Total Recovered",value=recovered)
            embed.add_field(name="Deaths",value=deaths)
            
        else:
            cases=covid.get_status_by_country_name(country)
            country=cases["country"]
            embed=discord.Embed(title=(f"{country}'s COVID-19 Statistics"))
            embed.add_field(name="Total Confirmed",value=cases["confirmed"])
            embed.add_field(name="Active",value=cases["active"])
            embed.add_field(name="New Cases",value=cases["new_cases"])
            embed.add_field(name="Total Recovered",value=cases["recovered"])
            embed.add_field(name="Tests Done", value=cases["total_tests"])
            embed.add_field(name="New Deaths",value=cases["new_deaths"])
            embed.add_field(name="Total Deaths",value=cases["deaths"])
            
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.RGtM0GjHmD-h-2vbkxXo_wHaE8?pid=Api&rs=1")
        await ctx.send(embed=embed)
    
    @covid.error
    async def clear_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(title="Unknown country, are you sure you spelled it correctly?"))
###########################################################################
    @commands.command(name="serverinfo", aliases=["s-info","server_info","server","servinfo"])
    async def serverinfo(self, ctx):
        members=0
        bots=0
        for member in ctx.guild.members:
            if member.bot:
                bots+=1
            else:
                members+=1
        
        roleCount=0
        for role in ctx.guild.roles:
            roleCount+=1
            
        embed=discord.Embed(title=str(ctx.guild), color=discord.Color.gold())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="Users",value=members)
        embed.add_field(name="Bots",value=bots)
        embed.add_field(name="Roles",value=roleCount)
        await ctx.send(embed=embed)
###########################################################################
    @commands.command(name="weather")
    async def weather(self, ctx, city):
        try:
            API_KEY=os.environ("WEATHER_API_KEY")
        except:
            config_object=ConfigParser()
            config_object.read("SentinelVariables.ini")
            variables=config_object["variables"]
            API_KEY=variables["WEATHER_API_KEY"]
        
        baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
        fullUrl = baseUrl + "appid=" + API_KEY + "&q=" + city
        response = requests.get(fullUrl) 

        responses = response.json() 

        if responses["cod"] == "404":
            await ctx.send("City not found! Be sure to correctly spell it")
        else:
            main = responses["main"] 
            currentTemperature = main["temp"] 
            tempC=round(currentTemperature-273.15,2) #Converts to celsius
            tempF=round(((9.0/5.0 * tempC) + 32),2)
            #currentPressure = main["pressure"] 
            #currentHumidity = main["humidity"] 
            weather = responses["weather"] 
            weather_description = weather[0]["description"] 

            embed=discord.Embed(title=("Current Weather in "+city), color=discord.Color.blue())
            embed.add_field(name="Temperature", value=(str(tempC)+"°C / "+str(tempF)+"°F"))
            embed.add_field(name="Weather",value=weather_description)
            await ctx.send(embed=embed)
    @weather.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to include the city you want to check! .s weather [city]")
###########################################################################
    @commands.command(name="temp", aliases=["tempconvert","tconvert","tcon"])
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
            newTemp=round(((temp - 32) * 5.0/9.0),2)
            title=(str(temp)+"° Fahrenheit is "+str(newTemp)+"° Celsius")
            
        else:
            newTemp=round(((9.0/5.0 * temp) + 32),2)
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
