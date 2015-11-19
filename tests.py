import os
import crimecast
import unittest
import tempfile
import datetime

from flask import json, jsonify

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from models import CrimeType, Crime, Week, Zip, drop_tables, create_tables

class CrimecastDBTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('postgresql://crimedata:poop@localhost/test')
        create_tables(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def tearDown(self):
        #pass

        self.session.commit()
        self.session.close()
        self.engine.execute(text('drop table crime cascade;'))
        self.engine.execute(text('drop table crime_type cascade;'))
        self.engine.execute(text('drop table week cascade;'))
        self.engine.execute(text('drop table zip cascade;'))
        drop_tables(self.engine)

    # -----------------
    # Crimes unit tests
    # -----------------

    def test_add_crime(self):
        query = self.session.query(Crime).all()
        start_size = len(query)

        self.session.add(Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of pig on building"))
        self.session.commit()
        query = self.session.query(Crime).all()

        end_size = len(query)

        self.assertEqual((start_size + 1), end_size)

    def test_find_crime(self):
        self.session.add(Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of pig on building"))
        self.session.commit()
        query = self.session.query(Crime).filter(Crime.address == "gdc").all()
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_find_crime_multiple(self):
        self.session.add(Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of pig on building"))
        self.session.add(Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of cow on building"))
        self.session.commit()
        query = self.session.query(Crime).filter(Crime.address == "gdc").all()
        q_size = len(query)

        self.assertEqual(q_size, 2)

    def test_crime_attributes(self):
        self.session.add(Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of pig on building"))
        self.session.add(Crime(lat=30.28500, lng=-97.7320000, time=datetime.date(year=2015, month=10, day=28), address="gdc", description="Graffiti of cow on building"))
        self.session.commit()
        query = self.session.query(Crime).filter(Crime.address == "gdc").first()

        self.assertEqual(query.description, "Graffiti of pig on building")

    # -----------------
    # Crime Types unit tests
    # -----------------

    def test_add_crime_type(self):
        query = self.session.query(CrimeType).all()
        start_size = len(query)

        self.session.add(CrimeType(name='Vandalism', desc = "Vandalism is bad"))
        self.session.commit()
        query = self.session.query(CrimeType).all()

        end_size = len(query)

        self.assertEqual((start_size + 1), end_size)

    def test_find_crime_type(self):
        self.session.add(CrimeType(name='Vandalism', desc = "Vandalism is bad"))
        self.session.commit()
        query = self.session.query(CrimeType).filter(CrimeType.name == "Vandalism").all()
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_crime_type_attributes(self):
        self.session.add(CrimeType(name='Vandalism', desc = "Vandalism is bad"))
        self.session.commit()
        query = self.session.query(CrimeType).filter(CrimeType.name == "Vandalism").first()

        self.assertEqual(query.desc, "Vandalism is bad")

    # -----------------
    # Zipcodes unit tests
    # -----------------

    def test_add_zipcode(self):
        query = self.session.query(Zip).all()
        start_size = len(query)

        self.session.add(Zip(zip_code=78704, lat=32.123, lng=32.123, pop=20000, family_income=50000))
        self.session.commit()
        query = self.session.query(Zip).all()

        end_size = len(query)

        self.assertEqual((start_size + 1), end_size)

    def test_find_zipcode(self):
        self.session.add(Zip(zip_code=78704, lat=32.123, lng=32.123, pop=20000, family_income=50000))
        self.session.commit()
        query = self.session.query(Zip).filter(Zip.pop == 20000).all()
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_find_zipcode_multiple(self):
        self.session.add(Zip(zip_code=78704, lat=32.123, lng=32.123, pop=20000, family_income=50000))
        self.session.add(Zip(zip_code=78705, lat=32.123, lng=32.123, pop=20000, family_income=40000))
        self.session.commit()
        query = self.session.query(Zip).filter(Zip.pop == 20000).all()
        q_size = len(query)

        self.assertEqual(q_size, 2)

    def test_zipcode_attributes(self):
        self.session.add(Zip(zip_code=78704, lat=32.123, lng=32.123, pop=20000, family_income=50000))
        self.session.add(Zip(zip_code=78705, lat=32.123, lng=32.123, pop=20000, family_income=50000))
        self.session.commit()
        query = self.session.query(Zip).filter(Zip.pop == 20000).first()

        self.assertEqual(query.family_income, 50000)

    # -----------------
    # Weeks unit tests
    # -----------------

    def test_add_week(self):
        query = self.session.query(Week).all()
        start_size = len(query)

        self.session.add(Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17)))
        self.session.commit()
        query = self.session.query(Week).all()

        end_size = len(query)

        self.assertEqual((start_size + 1), end_size)

    def test_find_week(self):
        self.session.add(Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17)))
        self.session.commit()
        query = self.session.query(Week).filter(Week.start == datetime.date(year=2015, month=10, day=11)).all()
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_find_week_multiple(self):
        self.session.add(Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17)))
        self.session.add(Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17)))
        self.session.commit()
        query = self.session.query(Week).filter(Week.start == datetime.date(year=2015, month=10, day=11)).all()
        q_size = len(query)

        self.assertEqual(q_size, 2)

    def test_week_attributes(self):
        self.session.add(Week(start=datetime.date(year=2015, month=10, day=11), end=datetime.date(year=2015, month=10, day=17)))
        self.session.add(Week(start=datetime.date(year=2015, month=10, day=18), end=datetime.date(year=2015, month=10, day=24)))
        self.session.commit()
        query = self.session.query(Week).filter(Week.start == datetime.date(year=2015, month=10, day=11)).first()

        self.assertEqual(query.end, datetime.datetime(year=2015, month=10, day=17, hour=0, minute=0))

class CrimecastAPITestCase(unittest.TestCase):

    def setUp(self):
        crimecast.app.config['TESTING'] = True
        self.app = crimecast.app.test_client()

    def tearDown(self):
        pass

    # -----------------
    # Splash unit tests
    # -----------------

    def test_splash_non_empty_response(self):
        rv = self.app.get('/')
        assert len(rv.data) > 0

    # -----------------
    # Crimes unit tests
    # -----------------

    def test_crimes_non_empty_response(self):
        rv = self.app.get('/api/v1/crimes')
        data = json.loads(rv.data)
        data = json.loads(data)
        assert len(data) > 0

    def test_crimes_has_id(self):
        rv = self.app.get('/api/v1/crimes/1040')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["crime_id"], "1040")

    def test_crimes_has_address(self):
        rv = self.app.get('/api/v1/crimes/1040')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["address"], "gdc")

    def test_crimes_has_type(self):
        rv = self.app.get('/api/v1/crimes/1040')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["crime_type"],  {'crime_type_id': '262',
                'desc': 'Vandalism is an action involving deliberate destruction of or damage to public or private property',
                'name': 'Vandalism',
                'worst_week': '770',
                'worst_zip': '246'
            })

    def test_crimes_has_zip(self):
        rv = self.app.get('/api/v1/crimes/1040')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["zip_code"], {'family_income': '41025',
                'lat': '30.274502199806',
                'lng': '-97.683778095778',
                'pop': '11482',
                'zip_code': '78721',
                'zip_id': '255'
            })

    def test_crimes_has_week(self):
        rv = self.app.get('/api/v1/crimes/1040')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["week"], {'end': '2015-10-24 00:00:00',
                'most_popular': '259',
                'start': '2015-10-18 00:00:00',
                'week_id': '769',
                'worst_zip': '246'
            })

    # ----------------------
    # Crime_Types unit tests
    # ----------------------

    def test_crime_types_non_empty_response(self):
        rv = self.app.get('/api/v1/crime_types')
        data = json.loads(rv.data)
        data = json.loads(data)
        assert len(data) > 0

    def test_crime_types_has_name(self):
        rv = self.app.get('/api/v1/crime_types/262')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["name"], "Vandalism")

    def test_crime_types_has_desc(self):
        rv = self.app.get('/api/v1/crime_types/262')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["desc"], "Vandalism is an action involving deliberate destruction of or damage to public or private property") # Testing here

    # ---------------
    # Zips unit tests
    # ---------------

    def test_zips_non_empty_response(self):
        rv = self.app.get('/api/v1/zips')
        data = json.loads(rv.data)
        data = json.loads(data)
        assert len(data) > 0

    def test_zips_has_id(self):
        rv = self.app.get('/api/v1/zips/268')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["zip_id"], "268")

    def test_zips_has_zip(self):
        rv = self.app.get('/api/v1/zips/268')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["zip_code"], "75735")

    def test_zips_has_lat(self):
        rv = self.app.get('/api/v1/zips/268')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["lat"], "30.240702922532")

    def test_zips_has_lng(self):
        rv = self.app.get('/api/v1/zips/268')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["lng"], "-97.835307667753")

    def test_zips_has_pop(self):
        rv = self.app.get('/api/v1/zips/268')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["pop"], "20000")

    def test_zips_has_family_income(self):
        rv = self.app.get('/api/v1/zips/268')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["family_income"], "50000")

    # ----------------
    # Weeks unit tests
    # ----------------

    def test_weeks_non_empty_response(self):
        rv = self.app.get('/api/v1/weeks')
        data = json.loads(rv.data)
        data = json.loads(data)
        assert len(data) > 0

    def test_weeks_has_id(self):
        rv = self.app.get('/api/v1/weeks/769')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["week_id"],  "769")

    def test_weeks_has_start_date(self):
        rv = self.app.get('/api/v1/weeks/769')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["start"], "2015-10-18 00:00:00")

    def test_weeks_has_end_date(self):
        rv = self.app.get('/api/v1/weeks/769')
        data = json.loads(rv.data)
        data = json.loads(data)
        self.assertEqual(data["end"], "2015-10-24 00:00:00")

if __name__ == '__main__':
    unittest.main() 
