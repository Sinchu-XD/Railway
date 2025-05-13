import requests
from pyrogram import filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("fare"))
    async def fare_enquiry(_, message: Message):
        if len(message.command) < 6:
            return await message.reply_text("Usage: /fare <train_no> <from> <to> <date YYYY-MM-DD> <class>")
        train_no = message.command[1]
        from_station = message.command[2].upper()
        to_station = message.command[3].upper()
        date = message.command[4]
        cls = message.command[5].upper()  # e.g. SL, 3A, 2A
        url = f"https://api.railwayapi.site/fare/{train_no}/{from_station}/{to_station}/{date}/{cls}"
        try:
            r = requests.get(url).json()
            fare = r.get("fare")
            quota = r.get("quota", "GN")
            if not fare:
                return await message.reply_text("🚫 Could not fetch fare.")
            await message.reply_text(f"💰 **Fare** for {cls} on {date}:\nTrain: {train_no}\nFrom: {from_station}\nTo: {to_station}\nQuota: {quota}\n\n💵 Amount: ₹{fare}")
        except:
            await message.reply_text("❌ Error fetching fare.")
          
