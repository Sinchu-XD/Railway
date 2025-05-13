import requests
from pyrogram import filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("pnr"))
    async def pnr_status(_, message: Message):
        if len(message.command) < 2:
            return await message.reply_text("Usage: /pnr <pnr_number>")
        pnr = message.command[1]

        url = f"https://api.railwayapi.site/pnr/{pnr}"
        try:
            r = requests.get(url).json()
            if r.get("error"):
                return await message.reply_text("🚫 Invalid or expired PNR.")

            train_name = r['train_name']
            train_number = r['train_number']
            from_station = r['from_station']['name']
            to_station = r['to_station']['name']
            doj = r['doj']
            chart_status = r.get("chart_prepared", "Unknown")

            text = f"🧾 **PNR Status**: `{pnr}`\n"
            text += f"🚆 **Train**: {train_name} ({train_number})\n"
            text += f"📍 **From**: {from_station} ➡️ **To**: {to_station}\n"
            text += f"📅 **Date**: {doj}\n"
            text += f"📊 **Chart Prepared**: {chart_status}\n\n"

            passengers = r.get("passengers", [])
            for idx, p in enumerate(passengers, 1):
                text += f"👤 Passenger {idx}: {p['current_status']} (Booking: {p['booking_status']})\n"

            await message.reply_text(text)
        except Exception:
            await message.reply_text("❌ Failed to fetch PNR details.")
          
