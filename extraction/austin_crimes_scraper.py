import requests
import json

if __name__ == "__main__":
    r = requests.get("https://data.austintexas.gov/resource/rkrg-9tez.json")
    data = r.json()
    final_crimes = []
    for crime in data:
        if 'latitude' in crime:
            final_crimes.append(crime)

    with open('other_crimes.out', 'w') as outfile:
        json.dump(final_crimes, outfile)
