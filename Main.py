import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

from Handlers import Available_Seats
from Handlers import Current_Station
from Handlers import Live_Station
from Handlers import Search_Stations
from Handlers import Search_Train
from Handlers import Train_Class
from Handlers import Trains_From_Station
from Handlers import fare_enquiry
from Handlers import pnr_status
from Handlers import schedule
from Handlers import train_status
from Handlers import trains_from_to


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("train_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

Available_Seats.register(app)
Current_Station.register(app)
Live_Station.register(app)
Search_Stations.register(app)
Search_Train.register(app)
Train_Class.register(app)
Trains_From_Station.register(app)
fare_enquiry.register(app)
pnr_status.register(app)
schedule.register(app)
train_status.register(app)
trains_from_to.register(app)

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("🚂 Welcome to the Train Info Bot! Type /help to see all available commands.")

@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    help_text = """
🤖 **Train Info Bot Commands**:

/start - Start the bot
/help - Show this help message

🔎 **Search Commands**
/searchstation <name/code> - Search stations by name or code
/searchtrain <train name/number> - Search trains by name or number

🚆 **Train Details**
/trainclasses <train_number> - Get available classes for a train
/schedule <train_number> - Get train schedule
/trainstatus <train_number> - Get current train status

📍 **Station & Route Info**
/stationtrains <station_code> - Trains from a specific station
/trainsbetweenstations <from> <to> - Trains between two stations
/current <train_no> [start_day (1-3)] - Get Where Is Your Train
/livestations <station_code> - Live status from a station

💺 **Booking & Seats**
/seat <train_no> <from> <to> <class> <date> <quota> - Check seat availability
/trainfare <train_no> <from_code> <to_code> - Fare inquiry

📄 **Other Utilities**
/pnrstatus <pnr_number> - Get PNR status
"""
    await message.reply(help_text)

if __name__ == "__main__":
    logger.info("Bot is starting...")
    app.run()
