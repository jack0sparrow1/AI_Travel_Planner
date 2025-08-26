from flask import Flask, render_template, request, jsonify
from planner.itinerary import generate_itinerary
from planner.flight_api import search_flights
from planner.hotel_api import get_hotels_by_city
from planner.location_api import get_iata_code
from google import genai
from config.settings import GEMINI_API_KEY, DEFAULT_MODEL

# ... your imports ...

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    itinerary = ""
    flights = []
    hotels = []
    error = None

    if request.method == "POST":
        destination_input = request.form.get("destination")
        days = int(request.form.get("days", 3))
        amount = request.form.get("budget")
        currency = request.form.get("currency", "")
        # Compose budget with currency symbol if provided
        budget = (f"{currency} {amount}".strip() if currency else (amount or ""))
        interests = request.form.get("interests")
        origin_input = request.form.get("origin")
        departure_date = request.form.get("departure_date")

        # Resolve IATA codes using your improved lookup
        origin_iata = get_iata_code(origin_input)
        destination_iata = get_iata_code(destination_input)

        if not origin_iata or not destination_iata:
            error = "Invalid origin or destination city. Please check your input."
        else:
            # Query flights and hotels APIs with resolved codes (limit results for speed)
            flights = search_flights(origin_iata, destination_iata, departure_date, adults=1, max_results=3) or []
            hotels = get_hotels_by_city(destination_iata) or []

            # Pass all gathered info to AI prompt orchestration
            itinerary = generate_itinerary(
                destination_input, days, budget, interests,
                origin_iata, destination_iata, flights, hotels
            )

    return render_template(
        "index.html",
        itinerary=itinerary,
        flights=flights,
        hotels=hotels,
        error=error,
        form_values=request.form
    )

@app.route("/api/famous-cities", methods=["GET"])
def famous_cities():
    country = request.args.get("country", "").strip()
    if not country:
        return jsonify({"error": "Missing 'country' parameter"}), 400

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
You are a travel data assistant. List the most famous cities in the country: {country}.
Return ONLY a JSON array of city names, no explanations. Limit to 8-12 items, diverse across regions.
Examples: ["Paris", "Lyon", "Nice"]
"""
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )
        text = (response.text or "").strip()

        # Normalize common code-fence formats from LLM output
        if text.startswith("```"):
            # Strip the first fence line and any trailing fence
            lines = text.splitlines()
            # drop first line like ```json
            if lines:
                lines = lines[1:]
            # remove trailing ``` if present
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        # Best-effort: ensure we return a JSON array
        import json
        cities = []
        try:
            # Try to parse direct JSON or extract array by brackets
            if not (text.startswith("[") and text.endswith("]")):
                # Find first '[' and last ']'
                start = text.find("[")
                end = text.rfind("]")
                if start != -1 and end != -1 and end > start:
                    text_candidate = text[start:end+1]
                else:
                    text_candidate = text
            else:
                text_candidate = text

            cities = json.loads(text_candidate)
            if not isinstance(cities, list):
                cities = []
        except Exception:
            # Fallback: try to extract lines
            for line in text.splitlines():
                line = line.strip("- •* \t\n\r ")
                if line and not line.startswith("[") and not line.startswith("`") and line.lower() != "json":
                    cities.append(line)

        # Clean and dedupe
        cleaned = []
        seen = set()
        for c in cities:
            name = str(c).strip()
            if name and name not in seen:
                seen.add(name)
                cleaned.append(name)

        if not cleaned:
            return jsonify({"error": "No cities found"}), 502

        return jsonify({"country": country, "cities": cleaned[:12]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)



# import streamlit as st
# from planner.itinerary import generate_itinerary
# from planner.flight_api import search_flights
# from planner.hotel_api import get_hotels_by_city
# from planner.location_api import get_iata_code
# from datetime import date

# st.title("🌍 AI Travel Planner")

# # User Inputs
# destination = st.text_input("Destination city (name or IATA code):", "TYO")
# days = st.number_input("Number of days:", min_value=1, max_value=30, value=3)
# budget = st.text_input("Budget (e.g., ₹80,000):", "₹80,000")
# interests = st.text_input("Interests (e.g., beaches, culture):", "culture")
# origin = st.text_input("Origin city (name or IATA code, e.g., DEL):", "DEL")
# departure_date = st.date_input("Departure date:", value=date.today())

# if st.button("Plan My Trip"):
#     with st.spinner("Generating itinerary..."):

#         departure_date_str = departure_date.strftime("%Y-%m-%d")

#         origin_code = origin if len(origin) == 3 else get_iata_code(origin)
#         destination_code = destination if len(destination) == 3 else get_iata_code(destination)

#         if not origin_code or not destination_code:
#             st.error("Could not resolve origin or destination to IATA code. Please check inputs.")
#         else:
#             flights = search_flights(origin_code, destination_code, departure_date_str, adults=1)
#             hotels_by_city = get_hotels_by_city(destination_code)
#             itinerary = generate_itinerary(destination, days, budget, interests, flights)

#             st.subheader("📝 Your Trip Itinerary")
#             st.markdown(itinerary)

#             if flights:
#                 st.subheader("✈️ Flight Options")
#                 for f in flights:
#                     price = f['price']['grandTotal']
#                     currency = f['price']['currency']
#                     route = " -> ".join(seg['departure']['iataCode'] for seg in f['itineraries'][0]['segments']) + " -> " + \
#                             f['itineraries'][0]['segments'][-1]['arrival']['iataCode']
#                     st.write(f"Route: {route} | Price: {price} {currency}")

#             if hotels_by_city:
#                 st.subheader("🏨 Sample Hotels")
#                 for hotel in hotels_by_city[:5]:
#                     st.write(f"{hotel['name']} — {', '.join(hotel['address'].get('lines', ['N/A']))}")
