import requests
from pyrogram import filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("trainstatus"))
    async def train_status(_, message: Message):
        if len(message.command) < 2:
            return await message.reply_text("Usage: /trainstatus <train_number>")
        train_number = message.command[1]
        url = f"https://api.railwayapi.site/live/train/{train_number}"
        try:
            r = requests.get(url).json()
            if r.get("error"):
                return await message.reply_text("🚫 Could not fetch train status.")
            text = f"🚆 **Train:** {r['train_name']} ({r['train_number']})\n"
            text += f"📍 **Current Position:** {r['position']}"
            await message.reply_text(text)
        except Exception as e:
            await message.reply_text("❌ Error fetching data.")
          
