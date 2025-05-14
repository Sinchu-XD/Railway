import requests
from pyrogram import Client, filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("pnrstatus"))
    async def pnrstatus(client, message: Message):
        try:
            pnr_number = message.text.split(" ", 1)[1]

            if not pnr_number.isdigit():
                await message.reply("❌ Please provide a valid PNR number.")
                return

            url = "https://irctc1.p.rapidapi.com/api/v2/getPNRStatus"
            querystring = {"pnrNumber": pnr_number}

            headers = {
                "x-rapidapi-key": "814d366d83msh97b8ba89155c2a8p140352jsn4c9a3b3bb565",
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            if response.status_code == 200:
                data = response.json().get("data", {})

                if not data:
                    await message.reply("❌ No data found for PNR status.")
                    return

                pnr = data.get("pnr_number")
                train_name = data.get("train_name")
                train_number = data.get("train_number")
                journey_date = data.get("journey_date")
                journey_duration = data.get("journey_duration")
                boarding_station = data.get("boarding_station", {}).get("station_name")
                departure_time = data.get("boarding_station", {}).get("departure_time")
                reservation_upto = data.get("reservation_upto", {}).get("station_name")
                passenger = data.get("passenger", [])[0]

                passenger_name = passenger.get("passengerName")
                passenger_status = passenger.get("currentStatusDisplayText")
                berth_no = passenger.get("currentBerthNo")
                berth_code = passenger.get("currentBerthCode")
                coach_id = passenger.get("currentCoachId")

                response_text = f"📑 PNR Status for {pnr}:\n"
                response_text += f"Train: {train_name} (Train No: {train_number})\n"
                response_text += f"Journey Date: {journey_date} | Duration: {journey_duration}\n"
                response_text += f"Boarding Station: {boarding_station} | Departure Time: {departure_time}\n"
                response_text += f"Reservation Up To: {reservation_upto}\n\n"
                response_text += f"🧑‍🤝‍🧑 Passenger Details:\n"
                response_text += f"Name: {passenger_name}\n"
                response_text += f"Berth No: {berth_no} | Berth Code: {berth_code} | Coach ID: {coach_id}\n"
                response_text += f"Booking Status: {passenger_status}\n\n"
                response_text += f"🎫 Ticket Status: Confirmed"

                await message.reply(response_text)
            else:
                await message.reply(f"⚠️ Error: Unable to fetch PNR status. HTTP Status Code: {response.status_code}")

        except IndexError:
            await message.reply("❌ Please provide a PNR number. Example: /pnrstatus 8813475598")
        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")
