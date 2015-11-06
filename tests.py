import os
import crimecast
import unittest
import tempfile
import datetime

from flask import json, jsonify

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from models import CrimeType, Crime, Week, Zip

class CrimecastDBTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('postgresql://crimedata:poop@localhost/test')
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        #pass
        self.session.close()
        Base.metadata.drop_all(self.engine)

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
        self.db_fd, crimecast.app.config['DATABASE'] = tempfile.mkstemp()
        crimecast.app.config['TESTING'] = True
        self.app = crimecast.app.test_client()
        # crimecast.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(crimecast.app.config['DATABASE'])

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
        assert len(data) > 0

    def test_crimes_has_id(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        self.assertEqual(data["crime_id"], "1")

    def test_crimes_has_address(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        self.assertEqual(data["address"], "GDC")

    def test_crimes_has_type(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        self.assertEqual(data["crime_type"], {
                'crime_type_id': '1',
                'name': 'Vandalism'
             })

    def test_crimes_has_zip(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        self.assertEqual(data["zip_code"], {
                'zip_id': '1',
                'zip_code': '78704'
            })

    def test_crimes_has_week(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        self.assertEqual(data["week"], {
                'week_id': '1',
                'start_date': '10/11/15'
            })

    # ----------------------
    # Crime_Types unit tests
    # ----------------------

    def test_crime_types_non_empty_response(self):
        rv = self.app.get('/api/v1/crime_types')
        data = json.loads(rv.data)
        assert len(data) > 0

    def test_crime_types_has_name(self):
        rv = self.app.get('/api/v1/crime_types/1')
        data = json.loads(rv.data)
        self.assertEqual(data["name"], "Vandalism")

    def test_crime_types_has_desc(self):
        rv = self.app.get('/api/v1/crime_types/1')
        data = json.loads(rv.data)
        self.assertEqual(data['name'], "Vandalism is bad") # Testing here

    # ---------------
    # Zips unit tests
    # ---------------

    def test_zips_non_empty_response(self):
        rv = self.app.get('/api/v1/zips')
        data = json.loads(rv.data)
        assert len(data) > 0

    def test_zips_has_id(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        self.assertEqual(data["zip_id"], "1")

    def test_zips_has_zip(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        self.assertEqual(data["zip_code"], "78704")

    def test_zips_has_lat(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        self.assertEqual(data["lat"], "32.123")

    def test_zips_has_lng(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        self.assertEqual(data["lng"], "32.123")

    def test_zips_has_pop(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        self.assertEqual(data["pop"], "12345")

    def test_zips_has_family_income(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        self.assertEqual(data["family_income"], "12345")

    # ----------------
    # Weeks unit tests
    # ----------------

    def test_weeks_non_empty_response(self):
        rv = self.app.get('/api/v1/weeks')
        data = json.loads(rv.data)
        assert len(data) > 0

    def test_weeks_has_id(self):
        rv = self.app.get('/api/v1/weeks/1')
        data = json.loads(rv.data)
        self.assertEqual(data["week_id"],  "1")

    def test_weeks_has_start_date(self):
        rv = self.app.get('/api/v1/weeks/1')
        data = json.loads(rv.data)
        self.assertEqual(data["start_date"], "10/11/15")

    def test_weeks_has_end_date(self):
        rv = self.app.get('/api/v1/weeks/1')
        data = json.loads(rv.data)
        self.assertEqual(data["end_date"], "10/17/15")

if __name__ == '__main__':
    unittest.main() 