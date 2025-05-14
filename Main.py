import os
import logging
from pyrogram import Client
from pyrogram.types import Message
from Handlers import search_station, search_train, get_train_classes, check_seat_availability, get_train_schedule, get_live_train_status, trains_between_stations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("train_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

search_station.register(app)
search_train.register(app)
get_train_classes.register(app)
check_seat_availability.register(app)
get_train_schedule.register(app)
get_live_train_status.register(app)
trains_between_stations.register(app)

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("🚂 Welcome to the Train Info Bot! Type /help to see all available commands.")

@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    help_text = """
    🤖 **Train Info Bot Commands**:
    
    /start - Start the bot
    /help - Show this help message
    /searchstation <station_code> - Search for station info by station code
    /searchtrain <train_number> - Search for train by train number
    /gettrainclasses <train_number> - Get available classes for a train
    /checkseataavailability <train_number> <from_station> <to_station> - Check seat availability
    /gettrainschedule <train_number> - Get the schedule for a train
    /getlivetrainstatus <train_number> - Get live status of a train
    /trainsbetweenstations <from_station> <to_station> - Get trains between two stations
    """
    await message.reply(help_text)

if __name__ == "__main__":
    logger.info("Bot is starting...")
    app.run()
