import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("livestations"))
    async def livestations(client, message: Message):
        try:
            hours = message.text.split(" ", 1)[1]

            if not hours.isdigit():
                await message.reply("❌ Please provide the number of hours. Example: /livestations 2")
                return

            url = "https://irctc1.p.rapidapi.com/api/v3/getLiveStation"
            querystring = {"hours": hours}

            headers = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") == "success" and data.get("data"):
                reply_text = f"🚉 Live Stations for the next {hours} hours:\n"
                for station in data["data"]:
                    reply_text += f"• {station['stationName']} - {station['trainCount']} trains\n"
                await message.reply(reply_text)
            else:
                await message.reply(f"❌ No live station data found for the next {hours} hours.")

        except IndexError:
            await message.reply("❌ Please provide the number of hours. Example: /livestations 2")
        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
          
