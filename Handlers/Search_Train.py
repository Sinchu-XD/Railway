import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("searchtrain"))
    async def search_train_handler(client: Client, message: Message):
        try:
            args = message.text.split(maxsplit=1)
            if len(args) != 2:
                await message.reply("❌ Usage: /searchtrain <query>")
                return

            query = args[1].strip()

            url = "https://irctc1.p.rapidapi.com/api/v1/searchTrain"
            querystring = {"query": query}

            headers = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("data"):
                reply = f"🚆 Trains matching '{query}':\n\n"
                for train in data["data"][:20]:
                    reply += f"🔹 {train['train_name']} ({train['train_number']})\n"
                await message.reply(reply)
            else:
                await message.reply("❌ No trains found.")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
          
