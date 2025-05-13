from pyrogram import Client, filters
from pyrogram.types import Message
from Handlers import train_status, pnr_status, trains_from_to, fare_enquiry, schedule

app = Client("train_bot", bot_token="7454714545:AAHIPQHGiujqJmWj-vbd4R3VJIBrjMX8GPM", api_id=6067591, api_hash="94e17044c2393f43fda31d3afe77b26b")

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("🚆 Welcome to Indian Railway Bot!\n\nUse commands like:\n/trainstatus\n/pnr\n/trainsfromto\n/fare\n/schedule")

# Register handlers
train_status.register(app)
trains_from_to.register(app)
fare_enquiry.register(app)
schedule.register(app)
pnr_status.register(app)

app.run()
