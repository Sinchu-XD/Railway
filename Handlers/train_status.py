import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("trainstatus"))
    async def trainstatus(client, message: Message):
        # Example: /trainstatus 12936
        try:
            # Fetching train number from the message
            train_no = message.text.split(" ", 1)[1]  # Get the train number after the command

            if not train_no.isdigit():
                await message.reply("❌ Please provide a valid train number.")
                return

            url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
            querystring = {"trainNo": train_no}

            headers = {
                "x-rapidapi-key": "814d366d83msh97b8ba89155c2a8p140352jsn4c9a3b3bb565",  # Replace with your actual key
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            # Fetch live train status data
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("status") == True and data.get("data"):
                train = data["data"]
                status_message = f"\n🚦 Live Status for {train.get('train_name')} ({train_no})"
                status_message += f"\n📍 Current Station: {train.get('current_station_name')} ({train.get('current_station_code')})"
                status_message += f"\n🕒 Last Updated: {train.get('updated_at')}"
                status_message += f"\n📈 Position: {train.get('position')}"
                await message.reply(status_message)
            else:
                await message.reply("❌ Failed to fetch live status or train not running today.")

        except IndexError:
            await message.reply("❌ Please provide a train number. Example: /trainstatus 12936")
        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
