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

zip_codes = [78610, 78613, 78617, 78641, 78652, 78653, 78660, 78664, 78681, 78701, 78702, 78703, 78704, 78705,\
            78712, 78717, 78719, 78721, 78722, 78723, 78724, 78725, 78726, 78727, 78728, 78729, 78730, 78731, \
            78732, 78733, 78734, 78735, 78736, 78737, 78738, 78739, 78741, 78742, 78744, 78745, 78746, 78747, \
            78748, 78749, 78750, 78751, 78752, 78753, 78754, 78756, 78757, 78758, 78759]

params = {'B00001': 'Total Population',
          'B02001': 'Race',
          'B01001': 'Sex by Age',
          'B11001': 'Household Type',
          'B17020': 'Poverty Status by age',
          'B19001': 'Household Income',
          'B19101': 'Family Income',
          'B19301': 'Per Capita Income',
          'B25002': 'Occupancy Status',
          'B25003': 'Tenure',
          'B25061': 'Rent Asked',
          'B25075': 'Value for owner-occupied units',
          'B25085': 'Price Asked for House',
          'B25104': 'Monthly housing cost'
          }


incomes = {
    '002E': 10000,
    '003E': 12500,
    '004E': 17500,
    '005E': 22500,
    '006E': 27500,
    '007E': 32500,
    '008E': 37500,
    '009E': 42500,
    '010E': 47500,
    '011E': 55000,
    '012E': 67500,
    '013E': 87000,
    '014E': 112500,
    '015E': 137500,
    '016E': 175000,
    '017E': 200000,
}

if __name__ == "__main__":
    data_file = open("extraction/zip_data.out")
    data = json.load(data_file)
    for zip in zip_codes:
        zip = str(zip)
        zip_data = data[zip]
        zipcode = session.query(Crime).from_statement(text('SELECT * FROM zip WHERE zip_code = :zip')).params(zip_code=zip).first()

        # Population
        pop = zip_data['B02001_001E'][0]['B02001_001E']
        zipcode.pop = int(pop)

        # Income
        num_asked = int(zip_data['B19001_001E'][0]['B19001_001E'])

        total = 0
        for param_end in incomes:
            param_key = 'B19001'
            param = param_key + '_' + param_end
            val = int(zip_data[param][0][param]) * incomes[param_end]
            total += val

        avg = 'Unknown'
        if num_asked != 0:
            avg = total//num_asked
        zipcode.family_income = avg


