from amadeus import Client, ResponseError
from config.settings import AMADUES_CLIENT_ID, AMADUES_CLIENT_SECRET

amadeus = Client(
    client_id=AMADUES_CLIENT_ID,
    client_secret=AMADUES_CLIENT_SECRET,
)

def search_flights(origin, destination, departure_date, adults=1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=adults,
            max=5
        )
        return response.data
    except ResponseError as error:
        print(f"Flight API error: {error}")
        return None

# Example usage:
if __name__ == "__main__":
    flights = search_flights("DEL", "BKK", "2025-09-10", 1)
    print(flights)
