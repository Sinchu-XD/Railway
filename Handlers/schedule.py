import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("schedule"))
    async def train_schedule(client, message: Message):
        try:
            args = message.text.split()
            if len(args) != 2:
                await message.reply("❌ Usage: /schedule <train_no>")
                return

            train_no = args[1]

            url = "https://irctc1.p.rapidapi.com/api/v1/getTrainSchedule"
            querystring = {"trainNo": train_no}

            headers = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") is True and data.get("data"):
                train = data["data"]
                reply_text = f"📅 Schedule for {train.get('train_name')} ({train_no}):\n\n"
                for station in train["route"]:
                    reply_text += (
                        f"🔸 {station['station_name']} ({station['station_code']})\n"
                        f"    ⏱️ Arrival: {station['arrival_time']} | Departure: {station['departure_time']}\n"
                        f"    ⏳ Halt: {station['halt']} min | Day: {station['day']}\n\n"
                    )
                await message.reply(reply_text)
            else:
                await message.reply("❌ Failed to fetch schedule. Check train number or try later.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
