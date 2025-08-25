from amadeus import Client, ResponseError
from config.settings import AMADUES_CLIENT_ID, AMADUES_CLIENT_SECRET

amadeus = Client(
    client_id=AMADUES_CLIENT_ID,
    client_secret=AMADUES_CLIENT_SECRET,
)

def search_flights(origin, destination, departure_date, adults=1, max_results=5):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=adults,
            max=max_results
        )
        return response.data
    except ResponseError as error:
        print(f"Flight API error: {error}")
        return None
