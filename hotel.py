from amadeus import Client, ResponseError
from config.settings import AMADUES_CLIENT_ID, AMADUES_CLIENT_SECRET

amadeus = Client(
    client_id=AMADUES_CLIENT_ID,
    client_secret=AMADUES_CLIENT_SECRET,
)

def get_hotels_by_city(city_code):
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=city_code)
        return response.data
    except ResponseError as error:
        print(f"Error fetching hotels by city: {error}")
        return None

# Example usage:
if __name__ == "__main__":
    hotels = get_hotels_by_city("PAR")  # Paris IATA city code
    print(hotels)
