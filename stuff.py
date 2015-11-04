import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db_connect, CrimeType, Crime, Week, Zip
engine = db_connect()
DBSession = sessionmaker(bind=engine)
#A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the 
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
  
# Insert a Person in the person table
def add():
    crime_1 = Crime(lat=30.28500, lng=-97.7320000, address="gdc", description="Graffiti of pig on building")
    crime_2 = Crime(lat=30.30000, lng=-97.730000, address="Duval Rd", description="Burglary at Quacks Bakery")
    crime_3 = Crime(lat=30.27000, lng=-97.719000, address="12th and Chicon", description="Murder on 12th and Chicon")
    crime_type_1 = CrimeType(name='Assault', desc = "Assault is bad")
    crime_type_2 = CrimeType(name='Burglary', desc = "Burglary is bad")
    crime_type_3 = CrimeType(name='Vandalism', desc = "Vandalism is bad")
    zip_1 = Zip(zipcode=78704, lat=32.123, lng=32.123, pop=5)
    zip_2 = Zip(zipcode=78705, lat=30.123, lng=30.123, pop=5)
    zip_3 = Zip(zipcode=78706, lat=35.123, lng=35.123, pop=5)
    week_1 = Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17))
    week_2 = Week(start=datetime.date(year=2015, month=10, day=18), end=datetime.date(year=2015, month=10, day=24))
    week_3 = Week(start=datetime.date(year=2015, month=10, day=25), end=datetime.date(year=2015, month=10, day=31))
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
    except:
        session.rollback()
        print("Everything broke")
    finally:
        session.close()

def read():
    person = session.query(CrimeType).all()
    print(len(person))
    print(str(person[11].name))
    session.close()

add()
