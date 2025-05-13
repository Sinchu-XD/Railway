import requests
from pyrogram import filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("trainsfromto"))
    async def trains_between(_, message: Message):
        if len(message.command) < 3:
            return await message.reply_text("Usage: /trainsfromto <from_station_code> <to_station_code>")
        from_station = message.command[1].upper()
        to_station = message.command[2].upper()
        url = f"https://api.railwayapi.site/between/{from_station}/{to_station}"
        try:
            r = requests.get(url).json()
            trains = r.get("trains", [])
            if not trains:
                return await message.reply_text("🚫 No trains found.")
            text = "🚉 **Trains Between Stations**:\n\n"
            for t in trains[:10]:  # Limit to 10
                text += f"🔹 {t['train_name']} ({t['train_number']}) - {t['src_departure_time']} to {t['dest_arrival_time']}\n"
            await message.reply_text(text)
        except:
            await message.reply_text("❌ Error fetching data.")
          
