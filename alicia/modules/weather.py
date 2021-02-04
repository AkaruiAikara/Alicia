from pyrogram import filters
from pytz import country_names as cname

from alicia import API_WEATHER, alia
from alicia.utils import AioHttp


@alia.on_message(filters.command("weather"))
async def weather(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await message.reply_text("Write a location to check the weather.")
        return
    split_city = args[1].split()
    CITY = "+".join(split_city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_WEATHER}"
    result = await AioHttp().get_json(url)
    if result["cod"] != 200:
        await message.reply_text("Location not valid.")
        return

    try:
        cityname = result["name"]
        curtemp = result["main"]["temp"]
        feels_like = result["main"]["feels_like"]
        humidity = result["main"]["humidity"]
        wind = result["wind"]["speed"]
        weath = result["weather"][0]
        icon = weath["id"]
        condmain = weath["main"]
        conddet = weath["description"]
        country_name = cname[f"{result['sys']['country']}"]
    except KeyError:
        await message.reply_text("Invalid Location!")
        return

    if icon <= 232:  # Rain storm
        icon = "⛈"
    elif icon <= 321:  # Drizzle
        icon = "🌧"
    elif icon <= 504:  # Light rain
        icon = "🌦"
    elif icon <= 531:  # Cloudy rain
        icon = "⛈"
    elif icon <= 622:  # Snow
        icon = "❄️"
    elif icon <= 781:  # Atmosphere
        icon = "🌪"
    elif icon <= 800:  # Bright
        icon = "☀️"
    elif icon <= 801:  # A little cloudy
        icon = "⛅️"
    elif icon <= 804:  # Cloudy
        icon = "☁️"
    kmph = str(wind * 3.6).split(".")

    def celsius(c):
        k = 273.15
        c = k if (c > (k - 1)) and (c < k) else c
        return str(round((c - k)))

    def fahr(c):
        c1 = 9 / 5
        c2 = 459.67
        tF = c * c1 - c2
        if tF < 0 and tF > -1:
            tF = 0
        return str(round(tF))

    text = f"**Current weather for {cityname}, {country_name} is**:\n\n**Temperature:** `{celsius(curtemp)}°C ({fahr(curtemp)}ºF), feels like {celsius(feels_like)}°C ({fahr(feels_like)}ºF)`\n**Condition:** `{condmain}, {conddet}` {icon}\n**Humidity:** `{humidity}%`\n**Wind:** `{kmph[0]} km/h`\n"
    await message.reply_text(text, parse_mode="markdown")


__help__ = """
Weather module:

 × /weather <city>: Gets weather information of particular place!
"""

__mod_name__ = "Weather"
