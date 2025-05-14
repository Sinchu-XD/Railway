import requess

def get_pnr_status(pnr_number):
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
            return "❌ No data found for this PNR."

        pnr = data.get("pnr_number")
        train_name = data.get("train_name")
        train_number = data.get("train_number")
        journey_date = data.get("journey_date")
        journey_duration = data.get("journey_duration")
        boarding_station = data.get("boarding_station", {}).get("station_name")
        departure_time = data.get("boarding_station", {}).get("departure_time")
        reservation_upto = data.get("reservation_upto", {}).get("station_name")

        passenger = data.get("passenger", [{}])[0]

        passenger_name = passenger.get("passengerName", "N/A")
        passenger_status = passenger.get("currentStatusDisplayText", "N/A")
        berth_no = passenger.get("currentBerthNo", "N/A")
        berth_code = passenger.get("currentBerthCode", "N/A")
        coach_id = passenger.get("currentCoachId", "N/A")

        response_text = f"📑 PNR Status for {pnr}:\n"
        response_text += f"Train: {train_name} (Train No: {train_number})\n"
        response_text += f"Journey Date: {journey_date} | Duration: {journey_duration}\n"
        response_text += f"Boarding: {boarding_station} | Departure: {departure_time}\n"
        response_text += f"To: {reservation_upto}\n\n"
        response_text += f"🧑‍🤝‍🧑 Passenger:\n"
        response_text += f"Name: {passenger_name}\n"
        response_text += f"Berth: {berth_no} ({berth_code}) | Coach: {coach_id}\n"
        response_text += f"Status: {passenger_status}\n"
        response_text += f"🎫 Ticket: Confirmed"

        return response_text
    else:
        return f"⚠️ Error: Unable to fetch PNR status. HTTP {response.status_code}"

# Command handler for /pnr
def register (app)
    @app.on_message(filters.command("pnr"))
    async def pnr_status_handler(client, message):
        if len(message.command) < 2:
            return await message.reply("❗ Usage: `/pnr <PNR_NUMBER>`", parse_mode="markdown")

        pnr_number = message.command[1]
        await message.reply("🔄 Fetching PNR status, please wait...")
        result = get_pnr_status(pnr_number)
        await message.reply(result)
