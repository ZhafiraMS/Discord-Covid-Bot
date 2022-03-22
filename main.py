from discord.ext import commands
from keep_alive import keep_alive
import os, discord, requests

bot = commands.Bot(command_prefix=".")
INVITE_URL = "https://discord.com/api/oauth2/authorize?client_id=955725599945666650&permissions=8&scope=bot"

@bot.event
async def on_ready():
    print("Bot active")

@bot.command()
async def summary(ctx):
    "worldwide summary"
    data = requests.get("https://api.covid19api.com/summary").json()['Countries']
    confirmed = 0
    deaths = 0
    recovered = 0
    topname = ''
    topcases = 0
    topdeaths = 0
    toprecovered = 0
    for place in data:
        c, d, r = place['TotalConfirmed'], place['TotalDeaths'], place['TotalRecovered']
        if c > topcases:
            topcases, topdeaths, toprecovered = c, d, r
            topname = place['Country']
        confirmed += c
        deaths += d
        recovered += r
    e = discord.Embed(title="Covid-19 Worldwide Summary")
    e.add_field(name="Confirmed Cases", value=confirmed)
    e.add_field(name="Deaths", value=deaths)
    e.add_field(name="Recovered", value=recovered)
    e.add_field(name="Top Country (by Cases)", value=topname, inline=False)
    e.add_field(name="Confirmed Cases", value=topcases)
    e.add_field(name="Deaths", value=topdeaths)
    e.add_field(name="Recovered", value=toprecovered)
    await ctx.send(embed=e)

@bot.command()
async def covid(ctx, *, content:str):
    "Stats for <country>"
    data = requests.get("https://api.covid19api.com/summary").json()['Countries']
    country = content.title()
    res = [x for x in data if x['Country'] == country]
    if res == []:
        await ctx.send("`Country [%s] not found`" % country)
        return
    res = res[0]
    e = discord.Embed(title="Summary of " + country)
    for name in res:
        e.add_field(name=name, value=res[name])
    await ctx.send(embed=e)

@bot.command()
async def dayone(ctx, *, content:str):
    "Returns all for a country. Argument must be country slug (use .country)"
    data = requests.get("https://api.covid19api.com/dayone/country/%s/status/confirmed" % content).json()
    if data == {}:
        await ctx.send("`Country [%s] not found" % content)
        return
    e = discord.Embed(title="Confirmed Cases for %s" % data[0]['Country'])
    for case in data:
        if len(e) >= 5900:
            break
        e.add_field(name="Province", value=(case['Province'] or case['Country']), inline=False)
        e.add_field(name="Coords", value=' '.join([str(case['Lat']), str(case['Lon'])]))
        e.add_field(name="Date", value=case['Date'])
        e.add_field(name="Cases", value=case['Cases'])
    await ctx.send(embed=e)

@bot.command()
async def quarantine(ctx):
    "Send quarantine info"
    e = discord.Embed(title="Quarantine Info")
    #e.set_image(url="https://www.sccmo.org/ImageRepository/Document?documentID=15321")
    e.set_image(url="https://i.imgur.com/sD2wSgu.jpg")
    await ctx.send(embed=e)

@bot.command()
async def wash(ctx):
    "How to wash your hands"
    e = discord.Embed(title="Wash your hands")
    e.set_image(url="https://images.squarespace-cdn.com/content/v1/56841850cbced6a015738a0a/1582828475817-ETA6CCQTIPIJDL5M4ON0/ke17ZwdGBToddI8pDm48kHSBwP7NGqkx6x3jg3IKfStZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpx4oGowBktfc-7vbo6j7dTPR3LZH3SqDGou0ipadpYn0ArYvvOQctY3IAEu8yNOVVw/how+to+wash+hands.png")
    await ctx.send(embed=e)

@bot.command()
async def spread(ctx):
    "Prevent spreading"
    e = discord.Embed(title="Prevent the spread")
    e.set_image(url="https://patch.com/img/cdn20/users/22874071/20200312/031120/styles/patch_image/public/estmwbvu4aablbs___12150228257.png")
    await ctx.send(embed=e)

@bot.command()
async def invite(ctx):
    "Get invite URL"
    e = discord.Embed(title="Covid-19-Bot", description="Made by Adika Prayata (666)")
    e.add_field(name="URL", value=INVITE_URL)
    e.set_footer(text="Hosted with 666VPS")
    await ctx.send(embed=e)

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("TOKEN"))