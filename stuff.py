import json
import os
import sys
import datetime
from geopy import Nominatim
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db_connect, CrimeType, Crime, Week, Zip
engine = db_connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()

crimes = []
weeks = []
zips = []
crime_types = []

def format_date(date):
    return datetime.strptime(date, "%m/%d/%y %H:%M %p")

def convert_year(date):
    return format_date(date).year

def convert_month(date):
    return format_date(date).month

def convert_day(date):
    return format_date(date).day

def transform_crime(next_crime_raw, date):
    converted_year = convert_year(date)
    converted_month = convert_month(date)
    converted_day = convert_day(date)
    return Crime(lat=next_crime_raw['lat'], lng=next_crime_raw['lon'], time=datetime.date(year=converted_year, month=converted_month, day=converted_day, address=next_crime_raw['address'], description=next_crime_raw['link']))

def transform_crime_type(next_crime_raw):
    return CrimeType(name=next_crime_raw['type'], desc='crimes are bad')

def transform_zip(next_crime_raw):
    geolocator = Nominatim()
    location = geolocator.reverse(str(next_crime_raw['lat'] + ", " + next_crime_raw['lon']))
    zip = location.raw['address']['postcode']
    boundingbox = location.raw['boundingbox']
    maxlat = float(boundingbox[1])
    minlat = float(boundingbox[0])
    maxlng = float(boundingbox[3])
    minlng = float(boundingbox[2])
    meanlat = (maxlat + minlat) / 2
    meanlng = (maxlng + minlng) / 2
    return Zip(zip_code=zip, lat=meanlat, lng=meanlng)

def transform_week(date):
    formatted_date = format_date(date)
    weekday = formatted_date.date().weekday()
    converted_year = convert_year(date)
    converted_month = convert_month(date)
    converted_day = convert_day(date)
    sunday = datetime(converted_year, converted_month, converted_day - weekday - 1)
    saturday = datetime(converted_year, converted_month, converted_day + (6 - weekday) - 1)
    return Week(start=sunday, end=saturday)

# Insert everything into the crimedata database
def add():
    with open("extraction/daily_spot_crime_data.json") as data_file:
        data = json.load(data_file)
    crime_data = iter(data['crimes'])
    for line in range(1):
        next_crime_raw = next(crime_data)
        date = next_crime_raw['date']

        next_crime = transform_crime(next_crime_raw, date)
        print(next_crime)
        next_crime_type = transform_crime_type(next_crime_raw)
        print(next_crime_type)
        next_zip = transform_zip(next_crime_raw)
        print(next_zip)
        next_week = transform_week(date)
        print(next_week)

        crimes.append(next_crime)
        crime_types.append(next_crime_type)
        zips.append(next_zip)
        weeks.append(next_week)

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

    #set up all of the foreign key relationships
    # print("Crime one week: " + str(week_1.start))
    try:
        for crime in crimes:
            session.add(crime)
        for crime_type in crime_types:
            session.add(crime_type)
        for zip in zips:
            session.add(zip)
        for week in weeks:
            session.add(week)
        # session.add(crime_1)
        # session.add(crime_2)
        # session.add(crime_3)
        # session.add(crime_type_1)
        # session.add(crime_type_2)
        # session.add(crime_type_3)
        # session.add(zip_1)
        # session.add(zip_2)
        # session.add(zip_3)
        # session.add(week_1)
        # session.add(week_2)
        # session.add(week_3)
        print("commiting to database")
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

def add_weeks_to_crimes():
    crimes = session.query(Crime).all()
    weeks = session.query(Week).all()
    try:
        for crime in crimes:
            for week in weeks:
                diff = crime.time - week.start
                if diff.days < 7 and diff.days > 0:
                    print(str(crime.time) + " : " + str(week.start))
                    crime.week = week.week_id
        session.commit()
        print("commiting to database")
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

def add_zips_to_crimes():
    crimes = session.query(Crime).all()
    zips = session.query(Zip).all()
    i = 0
    try:
        for crime in crimes:
            crime.zip_code = zips[i].zip_id
            print("adding zipcode " + str(zips[i].zip_id) + " to " + str(crime.description))
            i += 1
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

def add_crime_type_to_crimes():
    crimes = session.query(Crime).all()
    crime_types = session.query(CrimeType).all()
    i = 0
    try:
        for crime in crimes:
            crime.crime_type = crime_types[i].crime_type_id
            print("adding zipcode " + str(crime_types[i].crime_type_id) + " to " + str(crime.description))
            i += 1
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

#must be run after all of the crime data has been set up
def add_zip_to_week():
    weeks = session.query(Week).all()
    zip_codes = session.query(Zip).all()
    try:
        for week in weeks:
            most_pop = 0
            temp_zip = -1
            for zip_code in zip_codes:
                crimes = session.query(Crime).from_statement(text('SELECT * FROM crime WHERE zip_code = :zip_code')).params( zip_code=zip_code.zip_id).all()
                if len(crimes) > most_pop:
                    most_pop = len(crimes)
                    temp_zip = crimes[0].zip_code
            week.worst_zip = temp_zip
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")
    


#must be run after all of the crime data has been set up
def add_zip_to_crime_type():
    crime_types = session.query(CrimeType).all()
    zip_codes = session.query(Zip).all()
    try:
        for crime_type in crime_types:
            most_pop = 0
            temp_zip = -1
            for zip_code in zip_codes:
                crimes = session.query(Crime).from_statement(text('SELECT * FROM crime WHERE zip_code = :zip_code')).params( zip_code=zip_code.zip_id).all()
                if len(crimes) > most_pop:
                    most_pop = len(crimes)
                    temp_zip = crimes[0].zip_code
            crime_type.worst_zip = temp_zip
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

def add_week_to_crime_type():
    weeks = session.query(Week).all()
    crime_types = session.query(CrimeType).all()
    try:
        for crime_type in crime_types:
            most_pop = 0
            temp_week = -1
            for week in weeks:
                crimes = session.query(Crime).from_statement(text("SELECT * FROM crime WHERE week=:week and crime_type=:crime_type")).params(week=week.week_id, crime_type=crime_type.crime_type_id).all()
                print(len(crimes))
                if len(crimes) > most_pop:
                    most_pop = len(crimes)
                    temp_week = crimes[0].week
            crime_type.worst_week = temp_week
            print("adding week: " + str(crime_type.worst_week))
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

def add_crime_type_to_week(): 
    weeks = session.query(Week).all()
    crime_types = session.query(CrimeType).all()
    try:
        for crime_type in crime_types:
            for week in weeks:
                if crime_type.worst_week == week.week_id:
                    week.most_popular = crime_type.crime_type_id
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

def print_everything():
    crimes = session.query(Crime).all()
    print("crimes len: " + str(len(crimes)))
    weeks = session.query(Week).all()
    print("weeks len: " + str(len(weeks)))
    crime_types = session.query(CrimeType).all()
    print("crime_types len: " + str(len(crime_types)))
    zips = session.query(Zip).all()
    print("zips len: " + str(len(zips)))

add()
#add_weeks_to_crimes()
#add_zips_to_crimes()
#add_crime_type_to_crimes()
#add_zip_to_week()
#add_zip_to_crime_type()
#add_week_to_crime_type()
#add_crime_type_to_week()
print_everything()
session.close()
