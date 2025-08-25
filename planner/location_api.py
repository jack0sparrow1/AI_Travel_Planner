import os
import json

# Build absolute path to iata_codes.json relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'iata_codes.json')

with open(json_path, "r", encoding="utf-8") as f:
    IATA_MAP = json.load(f)
    
def get_iata_code(location_name: str) -> str:
    """Simple case-insensitive exact or partial match city name lookup to IATA code"""
    location_name_lower = location_name.strip().lower()
    
    # Exact match
    for city, code in IATA_MAP.items():
        if city.lower() == location_name_lower:
            return code
    
    # Partial or fuzzy match (starts with)
    for city, code in IATA_MAP.items():
        if city.lower().startswith(location_name_lower):
            return code
    
    return None
