import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("current"))
    async def live_train_status(client, message: Message):
        try:
            args = message.text.split()
            if len(args) < 2 or len(args) > 3:
                await message.reply("❌ Usage: /current <train_no> [start_day (1-3)]")
                return

            train_no = args[1]
            start_day = args[2] if len(args) == 3 else "1"

            url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
            querystring = {
                "trainNo": train_no,
                "startDay": start_day
            }

            headers = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") is True and data.get("data"):
                train = data["data"]
                reply = (
                    f"🚦 Live Status for {train.get('train_name')} ({train_no})\n\n"
                    f"📍 Current Station: {train.get('current_station_name')} ({train.get('current_station_code')})\n"
                    f"🕒 Last Updated: {train.get('updated_at')}\n"
                    f"📈 Position: {train.get('position')}"
                )
                await message.reply(reply)
            else:
                await message.reply("❌ Failed to fetch live status or train not running today.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
          
