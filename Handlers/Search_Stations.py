import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("searchstation"))
    async def search_station_handler(client: Client, message: Message):
        try:
            args = message.text.split(maxsplit=1)
            if len(args) != 2:
                await message.reply("❌ Usage: /searchstation <query>")
                return

            query = args[1].strip()

            url = "https://irctc1.p.rapidapi.com/api/v1/searchStation"
            querystring = {"query": query}

            headers = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",  # ⚠️ Replace with your actual key
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("data"):
                reply = f"🔎 Results for query '{query}':\n\n"
                for station in data["data"]:
                    reply += f"📍 {station['stationName']} ({station['stationCode']}) — {station['state']}\n"
                await message.reply(reply)
            else:
                await message.reply("❌ No stations found.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
          
