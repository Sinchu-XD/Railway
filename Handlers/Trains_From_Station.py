import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("stationtrains"))
    async def station_trains(client, message: Message):
        try:
            station_code = message.text.split(" ", 1)[1].upper()

            if not station_code.isalpha():
                await message.reply("❌ Please provide a valid station code. Example: /stationtrains NDLS")
                return

            url = "https://irctc1.p.rapidapi.com/api/v3/getTrainsByStation"
            querystring = {"stationCode": station_code}

            headers = {
                "x-rapidapi-key": "814d366d83msh97b8ba89155c2a8p140352jsn4c9a3b3bb565",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") == "success" and data.get("data"):
                reply_text = f"🚆 Trains from Station Code: {station_code}\n"
                for train in data["data"][:20]:
                    reply_text += f"• {train['trainNo']} - {train['trainName']}\n"
                await message.reply(reply_text)
            else:
                await message.reply(f"❌ No train data found for station {station_code}.")

        except IndexError:
            await message.reply("❌ Please provide a station code. Example: /stationtrains NDLS")
        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
