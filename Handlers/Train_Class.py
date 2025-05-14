import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("trainclasses"))
    async def train_classes(client, message: Message):
        try:
            args = message.text.split(" ", 1)
            if len(args) < 2:
                await message.reply("❌ Usage: /trainclasses <train_no>")
                return

            train_no = args[1]

            url = "https://irctc1.p.rapidapi.com/api/v1/getTrainClasses"
            querystring = {"trainNo": train_no}

            headers = {
                "x-rapidapi-key": "814d366d83msh97b8ba89155c2a8p140352jsn4c9a3b3bb565",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") and data.get("data"):
                reply_text = f"🚆 Available Classes for Train {train_no}:\n"
                for cls in data["data"]:
                    reply_text += f"• {cls.get('classCode')} - {cls.get('className')}\n"
                await message.reply(reply_text)
            else:
                await message.reply("❌ Could not fetch train classes. Please check the train number.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
          
