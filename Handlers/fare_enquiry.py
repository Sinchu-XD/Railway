import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("trainfare"))
    async def train_fare(client, message: Message):
        try:
            args = message.text.split(" ", 3)
            if len(args) < 4:
                await message.reply("❌ Usage: /trainfare <train_no> <from_code> <to_code>")
                return

            train_no = args[1]
            from_code = args[2].upper()
            to_code = args[3].upper()

            url = "https://irctc1.p.rapidapi.com/api/v2/getFare"
            querystring = {
                "trainNo": train_no,
                "fromStationCode": from_code,
                "toStationCode": to_code
            }

            headers = {
                "x-rapidapi-key": "814d366d83msh97b8ba89155c2a8p140352jsn4c9a3b3bb565",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") and data.get("data"):
                reply_text = f"💰 Fare Details for Train {train_no} ({from_code} → {to_code}):\n"
                for fare in data["data"]:
                    reply_text += f"• {fare['classType']} ({fare['className']}): ₹{fare['fare']}\n"
                await message.reply(reply_text)
            else:
                await message.reply("❌ Could not fetch train fare. Please check the parameters.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
