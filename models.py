import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
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
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(String(250), nullable=False)
    crimeType = Column(Integer, ForeignKey('CrimeType.crimeType_id'))
    time = Column(DateTime, nullable=False)
    description = Column(String(500))
    zip = Column(Integer, ForeignKey('Zip.zip_id'))
    week = Column(Integer, ForeignKey('Week.week_id'))

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
    worstZip = Column(Integer, ForeignKey('Zip.zip_id'))

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
    family_income = Column(Integer, nullable=False)


class CrimeType(Base):
    """
    Here we define columns for the table CrimeTypes.
    This model represents a type of crime, for instance 'Assault'
    """
    __tablename__ = 'CrimeType'
    crimeType_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    desc = Column(String(500), nullable=False)
    worstZip = Column(Integer, ForeignKey('Zip.zip_id'))
    # I think this is optional. just checking to see if it helps.
    def __repr__(self):
        return "<User(crimeType_id='%s', name='%s', desc='%s', worstarea='%f')>" % (
            self.crimeType_id, self.name, self.desc, self.worstArea)

    worstWeek = Column(Integer, ForeignKey('Week.week_id'))


# Create an engine that stores data in the local directory's
# stuff.db file.
def db_connect():
    engine = create_engine('postgresql://crimedata:poop@localhost/crimedata')
    return engine

 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
def create_tables(engine):
    Base.metadata.create_all(engine)

create_tables(db_connect())
 

# to run database:
# install postgresql (brew install postgresql)
# make sure that libpq-dev is installed (apt-get install libqp-dev)
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
