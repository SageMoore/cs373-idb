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

if __name__ == "__main__":
    crime_types = session.query(CrimeType).from_statement(text('SELECT * FROM crime_type')).all()

    for crime_type in crime_types:
        if crime_type.name == "Theft":
            crime_type.desc = "Theft is the taking of another person's property without that person's permission or consent with the intent to deprive the rightful owner of it"
        elif crime_type.name == "Shooting":
            crime_type.desc = "Shooting is the act or process of discharging firearms or other projectile weapons such as bows or crossbows"
        elif crime_type.name == "Robbery":
            crime_type.desc = "Robbery is the crime of taking or attempting to take anything of value by force or threat of force or by putting the victim in fear"
        elif crime_type.name == "Burglary":
            crime_type.desc = "Burglary is an unlawful entry into a building for the purposes of committing an offence"
        elif crime_type.name == "Vandalism":
            crime_type.desc = "Vandalism is an action involving deliberate destruction of or damage to public or private property"
        elif crime_type.name == "Assault":
            crime_type.desc = "Assault is harmful or offensive contact with a person"
        elif crime_type.name == "Arrest":
            crime_type.desc = "An arrest is the act of depriving a person of their liberty usually in relation to the purported investigation or prevention of crime and presenting (the arrestee) to a procedure as part of the criminal justice system"
        elif crime_type.name == "Other":
            crime_type.desc = "This covers any other types of crime"
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
