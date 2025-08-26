import csv
import json
import requests

# Download OpenFlights airports.dat CSV
url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
response = requests.get(url)
response.raise_for_status()

airports = []
reader = csv.reader(response.text.splitlines())

for row in reader:
    # OpenFlights columns: https://openflights.org/data.html
    # 0 id, 1 name, 2 city, 3 country, 4 IATA, 5 ICAO, 6 lat, 7 lon, 8 alt, 9 timezone, 10 DST, 11 tz database, 12 type, 13 source
    iata = row[4].strip()
    city = row[2].strip()
    country = row[3].strip()
    name = row[1].strip()
    if iata and iata != "\\N":  # valid IATA code
        airports.append({
            "city": city,
            "country": country,
            "iata": iata,
            "name": name
        })

# Save to JSON
with open("iata_codes_full.json", "w", encoding="utf-8") as f:
    json.dump(airports, f, indent=2, ensure_ascii=False)

print(f"Saved {len(airports)} airports to iata_codes_full.json")
