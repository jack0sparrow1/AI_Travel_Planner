from google import genai
from config.settings import GEMINI_API_KEY, DEFAULT_MODEL

def generate_itinerary(destination_input, days, budget, interests, origin_iata, destination_iata, flights, hotels):
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Format flights info for prompt
    flights_info = ""
    if flights:
        flights_info = "Flight Options Retrieved:\n"
        for f in flights:
            price = f.get('price', {}).get('grandTotal', 'N/A')
            currency = f.get('price', {}).get('currency', '')
            segments = f.get('itineraries', [{}])[0].get('segments', [])
            route = " -> ".join(segment.get('departure', {}).get('iataCode', '') for segment in segments)
            if segments:
                route += " -> " + segments[-1].get('arrival', {}).get('iataCode', '')
            flights_info += f"- Route: {route}, Price: {price} {currency}\n"
    else:
        flights_info = "No flight options found.\n"

    # Format hotels info similarly
    hotels_info = ""
    if hotels:
        hotels_info = "Hotel Options Retrieved:\n"
        for h in hotels[:5]:
            name = h.get('name', 'N/A')
            address = ", ".join(h.get('address', {}).get('lines', []))
            hotels_info += f"- {name}, Address: {address}\n"
    else:
        hotels_info = "No hotel options found.\n"

    prompt = f"""
You are a travel planner assistant.

User Input:
- Destination: {destination_input}
- Origin IATA: {origin_iata}
- Destination IATA: {destination_iata}
- Departure Date: [Use the provided app date if available]
- Days: {days}
- Budget: {budget}
- Interests: {interests}

{flights_info}
{hotels_info}

TASK: Produce a beautifully structured HTML itinerary. Use semantic headings and sections.
REQUIREMENTS:
- Answer with the currency given in the budget.
- Start with <section class="itinerary-header"> including an <h2> title and a short summary.
- Add a <section class="trip-facts"> with a small definition list (<dl>) for key facts (days, budget, interests, best flight pick, suggested hotel area).
- Add <section class="daily-plan"> with one <article class="day"> per day: include <h3> Day N and an unordered list of activities with brief descriptions and timing hints.
- Add <section class="tips"> with 5-7 bullet tips (local transport, safety, money, connectivity, cultural etiquette).
- Keep it concise, practical, and specific for the chosen destination.
- Do NOT include <html>, <head>, or <body> tags. Only the inner content sections.
"""

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt
    )

    return response.text
