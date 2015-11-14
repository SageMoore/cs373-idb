from datetime import datetime
# import geolocator as geolocator
from geopy.geocoders import Nominatim
import json
import re

__author__ = 'markdaniel'

def convert_year(date):
    return datetime.strptime(date, "%m/%d/%y %H:%M %p").year

def convert_month(date):
    return datetime.strptime(date, "%m/%d/%y %H:%M %p").month

def convert_day(date):
    return datetime.strptime(date, "%m/%d/%y %H:%M %p").day

crimes = []
weeks = []
zips = []
crime_types = []

with open("extraction/daily_spot_crime_data.json") as data_file:
    data = json.load(data_file)
    crime_data = iter(data['crimes'])
    for line in range(1):
        next_crime = next(crime_data)
        converted_year = convert_year(next_crime['date'])
        converted_month = convert_month(next_crime['date'])
        converted_day = convert_day(next_crime['date'])
        #
        # next_crime_formatted = Crime(lat=next_crime['lat'], lng=next_crime['lon'], time=datetime.date(year=converted_year, month=converted_month, day=converted_day, address=next_crime['address'], description=next_crime['link'])
        # next_crime_type = CrimeType(name=next_crime['type'], desc='crimes are bad')
        geolocator = Nominatim()
        location = geolocator.reverse("30.25, -97.75")

        zip = location.raw['address']['postcode']

        location = geolocator.geocode(str(zip))
        boundingbox = location.raw['boundingbox']
        maxlat = float(boundingbox[1])
        minlat = float(boundingbox[0])
        maxlng = float(boundingbox[3])
        minlng = float(boundingbox[2])
        meanlat = (maxlat + minlat) / 2
        meanlng = (maxlng + minlng) / 2

        #next_zip = Zip(zip_code=zip, lat=meanlat, lng=meanlng)
        #next_week = Week(
        print(next_crime)
        # crimes.append(next_crime_formatted)

    # for crime in crimes:
    #     print('crime: ' + str(crime))
        # session.add()

    # {"cdid":69098992,"lon":-97.8365453262,"lat":30.2111386727,"link":"http://spotcrime.com/crime/69098992-47f96dfb371686289c6415639b76305e","address":"3700 BLOCK OF KANDY DR","date":"10/19/15 09:07 PM","type":"Theft"},{"cdid":69111676,"lon":-97.835189,"lat":30.211453,"link":"http://spotcrime.com/crime/69111676-f1c8b43aee3dd74fcf16bd6e29cac415","address":"3700 BLOCK KANDY DR","date":"10/19/15 06:10 PM","type":"Theft"}
    #
    # crime_1 = Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of pig on building")
    # crime_2 = Crime(lat=30.30000, lng=-97.730000, time=datetime.date(year=2015, month=10, day=20), address="Duval Rd", description="Burglary at Quacks Bakery")
    # crime_3 = Crime(lat=30.27000, lng=-97.719000, time=datetime.date(year=2015, month=10, day=14), address="12th and Chicon", description="Murder on 12th and Chicon")
    # crime_type_1 = CrimeType(name='Vandalism', desc = "Vandalism is bad")
    # crime_type_2 = CrimeType(name='Burglary', desc = "Burglary is bad")
    # crime_type_3 = CrimeType(name='Assault', desc = "Assault is bad")
    # zip_1 = Zip(zip_code=78704, lat=32.123, lng=32.123, pop=20000, family_income=50000)
    # zip_2 = Zip(zip_code=78705, lat=30.123, lng=30.123, pop=23000, family_income=30000)
    # zip_3 = Zip(zip_code=78706, lat=35.123, lng=35.123, pop=19000, family_income=45000)
    # week_1 = Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17))
    # week_2 = Week(start=datetime.date(year=2015, month=10, day=18), end=datetime.date(year=2015, month=10, day=24))
    # week_3 = Week(start=datetime.date(year=2015, month=10, day=25), end=datetime.date(year=2015, month=10, day=31))