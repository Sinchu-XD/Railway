import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("trainsbetween"))
    async def trains_between(client: Client, message: Message):
        try:
            args = message.text.split()
            if len(args) != 3:
                await message.reply("❌ Usage: /trainsbetween <from_station> <to_station>")
                return

            from_station, to_station = args[1].upper(), args[2].upper()

            url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"
            querystring = {
                "fromStationCode": from_station,
                "toStationCode": to_station
            }

            headers = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("data"):
                trains = data["data"]
                reply = f"🚆 Trains from {from_station} to {to_station}:\n\n"
                for train in trains[:10]:
                    days = ", ".join([d["day_code"] for d in train["days"] if d["runs"] == "Y"])
                    reply += (
                        f"🔸 {train['train_name']} ({train['train_number']})\n"
                        f"⏰ Departure: {train['from_std']} | Arrival: {train['to_sta']}\n"
                        f"🕒 Duration: {train['duration']}\n"
                        f"📅 Runs on: {days}\n\n"
                    )
                await message.reply(reply)
            else:
                await message.reply("❌ No trains found between the given stations.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
