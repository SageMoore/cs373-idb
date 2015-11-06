import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db_connect, CrimeType, Crime, Week, Zip
engine = db_connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()
  
# Insert everything into the crimedata database
def add():
    crime_1 = Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of pig on building")
    crime_2 = Crime(lat=30.30000, lng=-97.730000, time=datetime.date(year=2015, month=10, day=20), address="Duval Rd", description="Burglary at Quacks Bakery")
    crime_3 = Crime(lat=30.27000, lng=-97.719000, time=datetime.date(year=2015, month=10, day=14), address="12th and Chicon", description="Murder on 12th and Chicon")
    crime_type_1 = CrimeType(name='Vandalism', desc = "Vandalism is bad")
    crime_type_2 = CrimeType(name='Burglary', desc = "Burglary is bad")
    crime_type_3 = CrimeType(name='Assault', desc = "Assault is bad")
    zip_1 = Zip(zip_code=78704, lat=32.123, lng=32.123, pop=20000, family_income=50000)
    zip_2 = Zip(zip_code=78705, lat=30.123, lng=30.123, pop=23000, family_income=30000)
    zip_3 = Zip(zip_code=78706, lat=35.123, lng=35.123, pop=19000, family_income=45000)
    week_1 = Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17))
    week_2 = Week(start=datetime.date(year=2015, month=10, day=18), end=datetime.date(year=2015, month=10, day=24))
    week_3 = Week(start=datetime.date(year=2015, month=10, day=25), end=datetime.date(year=2015, month=10, day=31))

    #set up all of the foreign key relationships
    print("Crime one week: " + str(week_1.start))
    try:
        session.add(crime_1)
        session.add(crime_2)
        session.add(crime_3)
        session.add(crime_type_1)
        session.add(crime_type_2)
        session.add(crime_type_3)
        session.add(zip_1)
        session.add(zip_2)
        session.add(zip_3)
        session.add(week_1)
        session.add(week_2)
        session.add(week_3)
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

#add()
#add_weeks_to_crimes()
#add_zips_to_crimes()
#add_crime_type_to_crimes()
#add_zip_to_week()
#add_zip_to_crime_type()
#add_week_to_crime_type()
#add_crime_type_to_week()
print_everything()
session.close()
