import requests
from pyrogram import filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("schedule"))
    async def schedule(_, message: Message):
        if len(message.command) < 2:
            return await message.reply_text("Usage: /schedule <train_no>")
        train_no = message.command[1]
        url = f"https://api.railwayapi.site/schedule/{train_no}"
        try:
            r = requests.get(url).json()
            text = f"📅 **Schedule for {r['train_name']} ({r['train_number']})**\n\n"
            for stop in r["route"][:10]:  # Limit to 10 stops
                text += f"🔹 {stop['station_name']} ({stop['station_code']}) - Arr: {stop['arrival_time']} Dep: {stop['departure_time']}\n"
            await message.reply_text(text)
        except:
            await message.reply_text("❌ Error fetching schedule.")
          
