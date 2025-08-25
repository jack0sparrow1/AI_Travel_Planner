from planner.itinerary import generate_itinerary
from planner.flight_api import search_flights
from planner.hotel_api import get_hotels_by_city
from planner.location_api import get_iata_code


def main():
    print("🌍 Welcome to AI Travel Planner v1!")

    destination = input("Enter destination city (name or IATA code): ").strip()
    days = int(input("Enter number of days: ").strip())
    budget = input("Enter budget (e.g., ₹50,000): ").strip()
    interests = input("Enter interests (e.g., beaches, nightlife, culture): ").strip()

    # For flights, ask origin and departure date
    origin = input("Enter your origin city (name or IATA code, e.g., DEL): ").strip()
    departure_date = input("Enter departure date (YYYY-MM-DD): ").strip()

    # Resolve IATA codes if not already codes
    origin_code = origin if len(origin) == 3 else get_iata_code(origin)
    destination_code = destination if len(destination) == 3 else get_iata_code(destination)

    if not origin_code or not destination_code:
        print("Invalid origin/destination name or code. Please try again.")
        return

    # Generate itinerary (without live flight/hotel data for now)
    print("\nGenerating your itinerary with preferences... Please wait ⏳\n")
    itinerary = generate_itinerary(destination, days, budget, interests)
    print("✅ Trip Itinerary:\n")
    print(itinerary)

    # Flights Search - use resolved IATA codes
    print("\nSearching flights...\n")
    flights = search_flights(origin_code, destination_code, departure_date, adults=1)
    if flights:
        print(f"Found {len(flights)} flight offers.")
        for flight in flights:
            price = flight['price']['grandTotal']
            currency = flight['price']['currency']
            route = " -> ".join(segment['departure']['iataCode'] for segment in flight['itineraries'][0]['segments']) + " -> " + \
                    flight['itineraries'][0]['segments'][-1]['arrival']['iataCode']
            print(f"Price: {price} {currency}, Route: {route}")
    else:
        print("No flights found.")

    # Hotel Search - use resolved city code
    print("\nLooking up hotels in the city...\n")
    hotels_by_city = get_hotels_by_city(destination_code)
    if hotels_by_city:
        print(f"Found {len(hotels_by_city)} hotels in {destination_code}. Sample:")
        for hotel in hotels_by_city[:5]:
            address_lines = hotel['address'].get('lines') if hotel['address'] else None
            address_str = ", ".join(address_lines) if address_lines else 'N/A'
            print(f" - {hotel['name']}, Address: {address_str}")
    else:
        print("No hotel details found for the city.")


if __name__ == "__main__":
    main()
