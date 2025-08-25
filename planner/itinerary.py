from google import genai
from config.settings import GEMINI_API_KEY, DEFAULT_MODEL
from planner.prompts import BASE_ITINERARY_PROMPT

def generate_itinerary(destination, days, budget, interests, flights=None, hotels=None):
    client = genai.Client(api_key=GEMINI_API_KEY)

    flights_info = ""
    if flights:
        flights_info = "Available flights:\n"
        for f in flights:
            price = f.get('price', {}).get('grandTotal', 'N/A')
            currency = f.get('price', {}).get('currency', '')
            segments = f.get('itineraries', [{}])[0].get('segments', [])
            route = " -> ".join(segment.get('departure', {}).get('iataCode', '') for segment in segments)
            if segments:
                route += " -> " + segments[-1].get('arrival', {}).get('iataCode', '')
            flights_info += f"- Route: {route}, Price: {price} {currency}\n"

    hotels_info = ""
    if hotels:
        hotels_info = "Available hotels:\n"
        for h in hotels:
            name = h.get('hotel', {}).get('name', 'N/A')
            address = h.get('hotel', {}).get('address', {}).get('lines', [''])[0]
            offers = h.get('offers', [{}])
            price = offers[0].get('price', {}).get('total', 'N/A') if offers else 'N/A'
            currency = offers[0].get('price', {}).get('currency', '') if offers else ''
            hotels_info += f"- {name}, Address: {address}, Price: {price} {currency} per night\n"

    prompt = f"""
You are an expert travel planner AI assistant.

Generate a concise, easy-to-follow day-by-day travel plan for {days} days in {destination}.

Budget: {budget}
Interests: {interests}

Use the following live flight and hotel options to inform your plan, but keep output brief with bullet points:

{flights_info}

{hotels_info}

Focus on practical activities, lodging, and transport ideas to make the trip seamless and enjoyable.
"""
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt
    )

    return response.text
