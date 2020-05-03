from get_data_methods import get_covid_data, get_rnumber_data, get_weather_data
import discord
import random
import datetime

def covid_output():

    covid_data = get_covid_data()
    procento_pozitiv_testu = int(covid_data['sick_count'].replace(" ", "")) / int(covid_data['test_count'].replace(" ", "")) * 100
    embed = discord.Embed(title=f'Covid-19', description=
        f"""Celkový počet provedených testů: **{covid_data["test_count"]}**  
Celkový počet osob s prokázanou nákazou **{covid_data["sick_count"]}** 
Celkový počet vyléčených: **{covid_data["recovered_count"]}**
Celkový počet úmrtí: **{covid_data["dead_count"]}**
Procento pozitivních testů: **{round(procento_pozitiv_testu, 2)} %**
Reprodukční číslo: **{get_rnumber_data()}**
K/D: **{round(int(covid_data["dead_count"].replace(" ","")) / int(covid_data["recovered_count"].replace(" ","")),2)}**
__{covid_data["uptime"]}__""")
    embed.colour = 9109643
    return embed


def weather_output(city):
    weather_data = get_weather_data(city)
    embed = discord.Embed(title=f'{weather_data["city_name"]}, {weather_data["city_state"]}', description=
f"""
**{weather_data["city_current_temp"]} °C**, **{weather_data["city_weather_status"]}**
**Pocitově: **{weather_data["city_feels_like"]} °C
**Max: **{weather_data["city_temp_max"]} °C, **Min: **{weather_data["city_temp_min"]} °C
**Východ slunce: **{weather_data["city_sunrise"]}
**Západ slunce: **{weather_data["city_sunset"]}
**{weather_data["city_datetime"]}**
    """)
    embed.colour = 8190976
    return embed

def news_output(data):
    articles = data
    output = []
    for article in articles:
        embed = discord.Embed(title=article["title"],
                              description=article["description"])
        embed.set_thumbnail(url=article["image"])
        embed.set_footer(icon_url="https://proxycache01-app.applytv.com/channel-data/0c190be96404efdd5535421ef936eb0e0864b3a1.png", text=f'Novinky.cz | {article["time"]}')
        embed.colour = 9109504
        output.append(embed)
    return output


def gaytest_output(ctx):
    if str(ctx.message.author)[-5:] == "#1926":
        roll = random.choice(range(50, 101))
        output = f"{ctx.message.author.mention} je {roll} % gay"
    else:
        roll = random.choice(range(0, 101))
        output = f"{ctx.message.author.mention} je {roll} % gay"
    embed = discord.Embed(title="Gay test", description=output)
    embed.colour = 16716947
    return embed

def playing_output(ctx, song_data):
    embed = discord.Embed(title=f'Právě hraje:', description=f"[{song_data['title']}]({song_data['url']})")
    embed.set_thumbnail(url=song_data["thumbnail"])
    embed.add_field(name="Autor:", value=f"[{song_data['uploader']}]({song_data['uploader_url']})")
    embed.add_field(name="Délka:", value=f'{str(datetime.timedelta(seconds=song_data["duration"]))}')
    embed.add_field(name="Žádáno od:", value=f'{ctx.message.author.mention}')
    embed.colour = 16776960
    return embed

def queue_output(ctx, song_data):
    embed = discord.Embed(title=f'Přidáno do fronty:', description=f"[{song_data['title']}]({song_data['url']})")
    embed.set_thumbnail(url=song_data["thumbnail"])
    embed.add_field(name="Autor:", value=f"[{song_data['uploader']}]({song_data['uploader_url']})")
    embed.add_field(name="Délka:", value=f'{str(datetime.timedelta(seconds=song_data["duration"]))}')
    embed.add_field(name="Žádáno od:", value=f'{ctx.message.author.mention}')
    embed.colour = 16776960
    return embed

async def songs_in_queue_output(ctx, queue):
    songs = ""
    queue_duration = 0
    for index, song in enumerate(queue[1:]):
        songs += f"**{index +1}**: {song['title']} \n"
        queue_duration += int(song["duration"])
        if (index + 1) % 20 == 0:
            embed = discord.Embed(title=f'Dále budou přehrány:', description=f"{songs}\n{str(datetime.timedelta(seconds=queue_duration))}\nŽádáno od: {ctx.message.author.mention}")
            embed.colour = 16776960
            await ctx.send(embed=embed)
            songs = ""

    embed = discord.Embed(title=f'Dále budou přehrány:', description=f"{songs}\n{str(datetime.timedelta(seconds=queue_duration))}\nŽádáno od: {ctx.message.author.mention}")
    embed.colour = 16776960
    await ctx.send(embed=embed)
    
def removed_song(ctx, song_data):
    embed = discord.Embed(title=f'Odebráno z fronty: ', description=f"[{song_data['title']}]({song_data['url']})")
    embed.add_field(name="Délka:", value=f'{str(datetime.timedelta(seconds=song_data["duration"]))}')
    embed.add_field(name="Žádáno od:", value=f'{ctx.message.author.mention}')
    embed.colour = 16776960
    return embed

async def songs_in_playlist_output(ctx, playlist):
    songs = ""
    playlist_name = ctx.message.content[9:]
    for index, song in enumerate(playlist):
        songs += f"{song['name']} \n"
        if (index + 1) % 20 == 0:
            embed = discord.Embed(title=f'{playlist_name}:', description=f"{songs} \nŽádáno od: {ctx.message.author.mention}")
            embed.colour = 16776960
            await ctx.send(embed=embed)
            songs = ""

    embed = discord.Embed(title=f'{playlist_name}:', description=f"{songs} \nŽádáno od: {ctx.message.author.mention}")
    embed.colour = 16776960
    await ctx.send(embed=embed)



