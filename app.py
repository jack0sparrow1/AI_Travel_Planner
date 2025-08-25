import streamlit as st
from planner.itinerary import generate_itinerary
from planner.flight_api import search_flights
from planner.hotel_api import get_hotels_by_city
from planner.location_api import get_iata_code
from datetime import date

st.title("🌍 AI Travel Planner")

# User Inputs
destination = st.text_input("Destination city (name or IATA code):", "TYO")
days = st.number_input("Number of days:", min_value=1, max_value=30, value=3)
budget = st.text_input("Budget (e.g., ₹80,000):", "₹80,000")
interests = st.text_input("Interests (e.g., beaches, culture):", "culture")
origin = st.text_input("Origin city (name or IATA code, e.g., DEL):", "DEL")
departure_date = st.date_input("Departure date:", value=date.today())

if st.button("Plan My Trip"):
    with st.spinner("Generating itinerary..."):

        departure_date_str = departure_date.strftime("%Y-%m-%d")

        origin_code = origin if len(origin) == 3 else get_iata_code(origin)
        destination_code = destination if len(destination) == 3 else get_iata_code(destination)

        if not origin_code or not destination_code:
            st.error("Could not resolve origin or destination to IATA code. Please check inputs.")
        else:
            flights = search_flights(origin_code, destination_code, departure_date_str, adults=1)
            hotels_by_city = get_hotels_by_city(destination_code)
            itinerary = generate_itinerary(destination, days, budget, interests, flights)

            st.subheader("📝 Your Trip Itinerary")
            st.markdown(itinerary)

            if flights:
                st.subheader("✈️ Flight Options")
                for f in flights:
                    price = f['price']['grandTotal']
                    currency = f['price']['currency']
                    route = " -> ".join(seg['departure']['iataCode'] for seg in f['itineraries'][0]['segments']) + " -> " + \
                            f['itineraries'][0]['segments'][-1]['arrival']['iataCode']
                    st.write(f"Route: {route} | Price: {price} {currency}")

            if hotels_by_city:
                st.subheader("🏨 Sample Hotels")
                for hotel in hotels_by_city[:5]:
                    st.write(f"{hotel['name']} — {', '.join(hotel['address'].get('lines', ['N/A']))}")
