import os
import json

# Load the full IATA codes JSON once on module load
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'iata_codes_full.json')  # your full file

with open(json_path, "r", encoding="utf-8") as f:
    IATA_DATA = json.load(f)  # List of dicts

def get_iata_code(city_or_code: str) -> str:
    """
    Return the IATA code for a city name or IATA code.
    Matches are found by:
    1. Exact IATA code (3-letter)
    2. Exact city name (case-insensitive)
    3. City name startswith input (partial match)
    4. Airport name containing the input (case-insensitive substring match)
    """
    city_or_code = city_or_code.strip()

    # 1. If input looks like a 3-letter code, return uppercase directly
    if len(city_or_code) == 3 and city_or_code.isalpha():
        return city_or_code.upper()

    city_lower = city_or_code.lower()

    # 2. Exact city match
    for entry in IATA_DATA:
        city = entry.get("city", "").lower()
        if city == city_lower:
            return entry.get("iata")

    # 3. Partial city match (startswith)
    for entry in IATA_DATA:
        city = entry.get("city", "").lower()
        if city.startswith(city_lower):
            return entry.get("iata")

    # 4. Airport name contains city input as substring
    for entry in IATA_DATA:
        airport_name = entry.get("name", "").lower()
        if city_lower in airport_name:
            return entry.get("iata")

    return None
