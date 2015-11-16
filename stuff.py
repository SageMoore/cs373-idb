import json
import os
import sys
from datetime import datetime, timedelta
from geopy import Nominatim
import re
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
count = 1200
sampling_index = 14


def format_date(date):
    return datetime.strptime(date, "%m/%d/%y %H:%M %p")

def convert_year(date):
    return format_date(date).year

def convert_month(date):
    return format_date(date).month

def convert_day(date):
    return format_date(date).day

def transform_crime(next_crime_raw, date, zip):
    converted_year = convert_year(date)
    converted_month = convert_month(date)
    converted_day = convert_day(date)
    return Crime(lat=next_crime_raw['lat'], lng=next_crime_raw['lon'], time=datetime(year=converted_year, month=converted_month, day=converted_day), address=str(next_crime_raw['address'] + ', ' + zip), description=next_crime_raw['link'])

def transform_crime_type(next_crime_raw):
    return CrimeType(name=next_crime_raw['type'], desc='crimes are bad')

def transform_zip(next_crime_raw):
    geolocator = Nominatim()
    location = geolocator.reverse(str(str(next_crime_raw['lat']) + ", " + str(next_crime_raw['lon'])))
    zip = location.raw['address']['postcode']
    location = geolocator.geocode(str(zip))
    boundingbox = location.raw['boundingbox']
    maxlat = float(boundingbox[1])
    minlat = float(boundingbox[0])
    maxlng = float(boundingbox[3])
    minlng = float(boundingbox[2])
    meanlat = (maxlat + minlat) / 2
    meanlng = (maxlng + minlng) / 2

    try:
        zip = re.search('^787d{2}$', zip).group(1)
        print('zip: ' + str(zip))
    except Exception:
        pass

    return Zip(zip_code=zip, lat=meanlat, lng=meanlng, pop=20000, family_income=50000)

def transform_week(date):
    formatted_date = format_date(date)
    weekday = formatted_date.date().weekday()
    # Need to adjust to use Sunday based indexing rather than Monday
    sunday = formatted_date - timedelta(days=((weekday + 1) % 7))
    sunday = sunday.replace(hour=00, minute=00, second=00)
    saturday = sunday + timedelta(days=6)
    saturday = saturday.replace(hour=00, minute=00, second=00)
    return Week(start=sunday, end=saturday)

def get_zip(next_crime_raw):
    geolocator = Nominatim()
    location = geolocator.reverse(str(str(next_crime_raw['lat']) + ", " + str(next_crime_raw['lon'])))
    return location.raw['address']['postcode']

def transform_data(data, count, sampling_index):
    crime_data = iter(data['crimes'])
    for line in range(count):
        next_crime_raw = next(crime_data)
        if line % sampling_index == 0:
            date = next_crime_raw['date']

            zip = get_zip(next_crime_raw)
            # print(str(zip))

            if (len(str(zip)) == 5):
                next_crime = transform_crime(next_crime_raw, date, zip)
                # print(next_crime)
                next_crime_type = transform_crime_type(next_crime_raw)
                # print(next_crime_type)
                next_zip = transform_zip(next_crime_raw)
                # print(next_zip)
                next_week = transform_week(date)
                # print(next_week)

                crimes.append(next_crime)
                crime_types.append(next_crime_type)
                zips.append(next_zip)
                weeks.append(next_week)

# Insert everything into the crimedata database
def add():

    with open("extraction/daily_spot_crime_data.json") as data_file:
        data = json.load(data_file)
    transform_data(data, count, sampling_index)
    with open("extraction/daily_spot_crime_data2.json") as data_file:
        data = json.load(data_file)
    transform_data(data, count, sampling_index)

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
    # # print("Crime one week: " + str(week_1.start))
    # print('crime_len: ' + str(len(crimes)))
    # print('crime_type_len: ' + str(len(crime_types)))
    # print('zip len: '  + str(len(zips)))

    try:
        for crime in crimes:
            # print(crime)
            if session.query(Crime).filter_by(description=crime.description).count() == 0:
                print('adding crime')
                session.add(crime)
            else:
                print('already added: ' + str(crime.description))
        for crime_type in crime_types:
            if session.query(CrimeType).filter_by(name=crime_type.name).count() == 0:
                session.add(crime_type)
            else:
                print('already added: ' + str(crime_type.name))
        for zip in zips:
            if session.query(Zip).filter_by(zip_code=zip.zip_code).count() == 0:
                session.add(zip)
            else:
                print('already added: ' + str(zip.zip_code))
        for week in weeks:
            if session.query(Week).filter_by(start=week.start).count() == 0:
                session.add(week)
            else:
                print('already added: ' + str(week.start))

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

def add_all_crime_types_to_crimes(data, count):
    crime_data = iter(data['crimes'])
    # crimes = session.query(Crime).all()
    crime_types = session.query(CrimeType).all()
    i = 0
    try:
        for crime in range(count):
            next_crime_raw = next(crime_data)
            if crime % 7 == 0:
                zip = get_zip(next_crime_raw)
                if (len(str(zip)) == 5):
                    crime_type_id = session.query(CrimeType.crime_type_id).filter_by(name=str(next_crime_raw['type'])).all()[0][0]
                    # print('crime_type_id: ' + str(crime_type_id[0][0]))
                    db_crime = session.query(Crime).filter_by(description=next_crime_raw['link']).all()[0]
                    # print('db_crime: ' + str(db_crime[0]))
                    db_crime.crime_type = crime_type_id
                    # print("adding zipcode " + str(crime_types[i].crime_type_id) + " to " + str(crime.description))
                    i += 1

        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        print("Everything broke")

def add_crime_type_to_crimes():
    with open("extraction/daily_spot_crime_data.json") as data_file:
        data = json.load(data_file)
    add_all_crime_types_to_crimes(data, count - 10)
    with open("extraction/daily_spot_crime_data2.json") as data_file:
        data = json.load(data_file)
    add_all_crime_types_to_crimes(data, count - 10)


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
add_crime_type_to_crimes()
#add_zip_to_week()
#add_zip_to_crime_type()
#add_week_to_crime_type()
#add_crime_type_to_week()
print_everything()
session.close()
