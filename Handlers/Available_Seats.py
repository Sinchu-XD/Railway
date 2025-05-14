import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("seat"))
    async def seat_availability(client, message: Message):
        try:
            args = message.text.split()
            if len(args) < 4:
                await message.reply("❌ Usage: /seat <train_no> <from_code> <to_code> [class_type] [quota]")
                return

            train_no = args[1]
            from_code = args[2]
            to_code = args[3]
            class_type = args[4] if len(args) > 4 else "2A"
            quota = args[5] if len(args) > 5 else "GN"

            url = "https://irctc1.p.rapidapi.com/api/v1/checkSeatAvailability"
            querystring = {
                "classType": class_type,
                "fromStationCode": from_code,
                "toStationCode": to_code,
                "quota": quota,
                "trainNo": train_no
            }

            headers = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") and data.get("data"):
                reply_text = f"🪑 Seat Availability for Train {train_no} ({class_type}, Quota: {quota}):\n"
                for day in data["data"]:
                    reply_text += f"📅 {day['date']}: {day['current_status']}\n"
                await message.reply(reply_text)
            else:
                await message.reply("❌ Could not fetch seat availability. Check parameters or try again later.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
          
