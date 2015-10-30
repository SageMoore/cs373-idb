import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Crime(Base):
    """
    Here we define columns for the table Crime
    This model represents all the information contained about a crime.
    Some of the extra fields here are foreign keys because many other models contain Crimes.
    """
    __tablename__ = 'Crime'
    crime_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(String(250), nullable=False)
    crimeTypeId = Column(Integer, ForeignKey('CrimeType.crimeType_id'))
    time = Column(DateTime, nullable=False)
    description = Column(String(500))
 
class Week(Base):
    """
    Here we define columns for the table Week.
    This model represents a particular week, for instance 1-1-15 through 1-7-15
    """
    __tablename__ = 'Week'
    week_id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    mostPopular = Column(Integer, ForeignKey('CrimeType.crimeType_id'))

class Zip(Base):
    """
    Here we define columns for the table Zip.
    This model represents a zipcode in Austin, for instance 78705
    """
    __tablename__ = 'Zip'
    zip_id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    pop = Column(Integer, nullable=False)
    crimeId = Column(Integer, ForeignKey('Crime.crime_id'))


class CrimeType(Base):
    """
    Here we define columns for the table CrimeTypes.
    This model represents a type of crime, for instance 'Assault'
    """
    __tablename__ = 'CrimeType'
    crimeType_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    desc = Column(String(500), nullable=False)
    worstArea = Column(Integer, ForeignKey('Zip.zip_id'))



# Create an engine that stores data in the local directory's
# stuff.db file.
engine = create_engine('postgres://localhost:8080/postgres')

 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
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
new_crime_type = CrimeType(name='new person', desc = "poop" )
session.add(new_crime_type)
session.commit()

session.query(CrimeType).all()
person = session.query(CrimeType).first()
print(person.name)
# Insert an Address in the address table
# to run database:
# install postgresql (brew install postgresql)
# install psycopg2 (pip3 install psycopg2)
# init postgres server (pg_ctl init -D database)
# run postgres server (postgres -D database/ -p 8080)


# To connect to db and execute csommand
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# engine = create_engine('postgres://localhost:8080/postgres')
# session = sessionmaker(bind=engine)()
# result = session.execute('select * from test where id=1')
# for row in result:
#     print(row)
