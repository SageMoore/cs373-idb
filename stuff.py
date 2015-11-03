import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db_connect, CrimeType
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

    new_crime_type = CrimeType(name='new person 3', desc = "poop")
    try:
        session.add(new_crime_type)
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

read()
