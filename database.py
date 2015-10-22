import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Crime(Base):
    __tablename__ = 'Crime'
    # Here we define columns for the table Crime
    # Notice that each column is also a normal Python instance attribute.
    crime_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(String(250), nullable=False)
    crimeTypeId = Column(Integer, ForeignKey('CrimeType.crimeType_id'))
    time = Column(DateTime, nullable=False)
    description = Column(String(500))
 
class Week(Base):
    __tablename__ = 'Week'
    # Here we define columns for the table Week.
    # Notice that each column is also a normal Python instance attribute.
    week_id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    mostPopular = Column(Integer, ForeignKey('CrimeType.crimeType_id'))

class Zip(Base):
    __tablename__ = 'Zip'
    # Here we define columns for the table Zip.
    # Notice that each column is also a normal Python instance attribute.
    zip_id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    pop = Column(Integer, nullable=False)
    crimeId = Column(Integer, ForeignKey('Crime.crime_id')


class CrimeType(Base):
    __tablename__ = 'CrimeType'
    # Here we define columns for the table CrimeTypes.
    # Notice that each column is also a normal Python instance attribute.
    crimeType_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    desc = Column(String(500), nullable=False)
    worstArea = Column(Integer, ForeignKey('Area.area_id'))



# Create an engine that stores data in the local directory's
# stuff.db file.
engine = create_engine('mysql:///stuff.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
