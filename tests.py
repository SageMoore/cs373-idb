import os
import crimecast
import unittest
import tempfile

from flask import json, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import db_connect, CrimeType, Crime, Week, Zip

class CrimecastDBTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('postgresql://crimedata:poop@localhost/test')
        self.DBSession = sessionmaker(bind=engine)
        self.session = self.DBSession()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    # -----------------
    # Crimes unit tests
    # -----------------

    def test_add_crime(self):
        query = self.session.query(Crime).all()
        start_size = len(query)

        self.session.add(Crime(name="crime", lat=43.21, lng=12.34, addres="123 place",
                               crimeType=1, time="11/11/11", description="asdf", zip=1, week=1))
        self.session.commit()
        query = self.session.query(Crime).all()

        end_size = len(query)

        self.assertEqual(start_size + 1, end_size)

    def test_find_crime(self):
        self.session.add(Crime(name="crime", lat=43.21, lng=12.34, addres="123 place",
                               crimeType=1, time="11/11/11", description="asdf", zip=1, week=1))
        self.session.commit()
        query = self.session.query(Crime).filter(Crime.name == "crime")
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_find_crime_multiple(self):
        self.session.add(Crime(name="crime", lat=43.21, lng=12.34, addres="123 place",
                               crimeType=1, time="11/11/11", description="asdf", zip=1, week=1))
        self.session.add(Crime(name="crime", lat=43.21, lng=12.34, addres="123 place",
                               crimeType=1, time="11/11/11", description="fdsa", zip=1, week=1))
        self.session.commit()
        query = self.session.query(Crime).filter(Crime.name == "crime")
        q_size = len(query)

        self.assertEqual(q_size, 2)

    def test_crime_attributes(self):
        self.session.add(Crime(name="crime", lat=43.21, lng=12.34, addres="123 place",
                               crimeType=1, time="11/11/11", description="asdf", zip=1, week=1))
        self.session.add(Crime(name="crime2", lat=43.21, lng=12.34, addres="123 place",
                               crimeType=1, time="11/11/11", description="fdsa", zip=1, week=1))
        self.session.commit()
        query = self.session.query(Crime).filter(Crime.name == "crime").first()

        self.assertEqual(query.description, "asdf")

    # -----------------
    # Crime Types unit tests
    # -----------------

    def test_add_crime_type(self):
        query = self.session.query(CrimeType).all()
        start_size = len(query)

        self.session.add(CrimeType(name="crimetype", desc="asdf", worstArea=1, worst_week=1))
        self.session.commit()
        query = self.session.query(CrimeType).all()

        end_size = len(query)

        self.assertEqual(start_size + 1, end_size)

    def test_find_crime_type(self):
        self.session.add(CrimeType(name="crimetype", desc="asdf", worstArea=1, worst_week=1))
        self.session.commit()
        query = self.session.query(CrimeType).filter(CrimeType.name == "crimetype")
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_find_crime_type_multiple(self):
        self.session.add(CrimeType(name="crimetype", desc="asdf", worstArea=1, worst_week=1))
        self.session.add(CrimeType(name="crimetype", desc="fdsa", worstArea=1, worst_week=1))
        self.session.commit()
        query = self.session.query(CrimeType).all()
        q_size = len(query)

        self.assertEqual(q_size, 2)

    def test_crime_type_attributes(self):
        self.session.add(CrimeType(name="crimetype", desc="asdf", worstArea=1, worst_week=1))
        self.session.add(CrimeType(name="crimetype2", desc="fdas", worstArea=1, worst_week=1))
        self.session.commit()
        query = self.session.query(CrimeType).filter(CrimeType.name == "crimetype").first()

        self.assertEqual(query.description, "asdf")

    # -----------------
    # Zipcodes unit tests
    # -----------------

    def test_add_zipcode(self):
        query = self.session.query(Zip).all()
        start_size = len(query)

        self.session.add(Zip(lat=43.21, lng=12.34, pop=12345, family_income=12345))
        self.session.commit()
        query = self.session.query(Zip).all()

        end_size = len(query)

        self.assertEqual(start_size + 1, end_size)

    def test_find_zipcode(self):
        self.session.add(Zip(lat=43.21, lng=12.34, pop=12345, family_income=12345))
        self.session.commit()
        query = self.session.query(Zip).filter(Zip.pop == 12345)
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_find_zipcode_multiple(self):
        self.session.add(Zip(lat=43.21, lng=12.34, pop=12345, family_income=12345))
        self.session.add(Zip(lat=43.21, lng=12.34, pop=12345, family_income=12345))
        self.session.commit()
        query = self.session.query(Zip).filter(Zip.pop == 12345)
        q_size = len(query)

        self.assertEqual(q_size, 2)

    def test_zipcode_attributes(self):
        self.session.add(Zip(lat=43.21, lng=12.34, pop=12345, family_income=12345))
        self.session.add(Zip(lat=43.21, lng=12.34, pop=12345, family_income=12345))
        self.session.commit()
        query = self.session.query(Zip).filter(Zip.pop == 12345).first()

        self.assertEqual(query.description, "asdf")

    # -----------------
    # Weeks unit tests
    # -----------------

    def test_add_week(self):
        query = self.session.query(Week).all()
        start_size = len(query)

        self.session.add(Week(start="11/11//11", end="11/17/11", mostPopular=1, worst_zip=1))
        self.session.commit()
        query = self.session.query(Week).all()

        end_size = len(query)

        self.assertEqual(start_size + 1, end_size)

    def test_find_week(self):
        self.session.add(Week(start="11/11//11", end="11/17/11", mostPopular=1, worst_zip=1))
        self.session.commit()
        query = self.session.query(Week).filter(Week.pop == "crime")
        q_size = len(query)

        self.assertEqual(q_size, 1)

    def test_find_week_multiple(self):
        self.session.add(Week(start="11/11//11", end="11/17/11", mostPopular=1, worst_zip=1))
        self.session.add(Week(start="11/11//11", end="11/17/11", mostPopular=1, worst_zip=1))
        self.session.commit()
        query = self.session.query(Week).filter(Week.start == "11/11/11")
        q_size = len(query)

        self.assertEqual(q_size, 2)

    def test_week_attributes(self):
        self.session.add(Week(start="11/11//11", end="11/17/11", mostPopular=1, worst_zip=1))
        self.session.add(Week(start="11/11//11", end="11/17/11", mostPopular=1, worst_zip=1))
        self.session.commit()
        query = self.session.query(Week).filter(Week.start == "11/11/11").first()

        self.assertEqual(query.description, "asdf")


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
        assert data["crime_id"] == "1"

    def test_crimes_has_address(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        assert data["address"] == "GDC"

    def test_crimes_has_type(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        assert data["crime_type"] == {
                'crime_type_id': '1',
                'name': 'Vandalism'
             }

    def test_crimes_has_zip(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        assert data["zip_code"] == {
                'zip_id': '1',
                'zip_code': '78704'
            }

    def test_crimes_has_week(self):
        rv = self.app.get('/api/v1/crimes/1')
        data = json.loads(rv.data)
        assert data["week"], {
                'week_id': '1',
                'start_date': '10/11/15'
            }

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
        assert data["name"] == "Vandalism"

    def test_crime_types_has_desc(self):
        rv = self.app.get('/api/v1/crime_types/1')
        data = json.loads(rv.data)
        assert data["desc"] == "Vandalism is bad"

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
        assert data["zip_id"] == "1"

    def test_zips_has_zip(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        assert data["zip_code"] == "78704"

    def test_zips_has_lat(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        assert data["lat"] == "32.123"

    def test_zips_has_lng(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        assert data["lng"] == "32.123"

    def test_zips_has_pop(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        assert data["pop"] == "12345"

    def test_zips_has_family_income(self):
        rv = self.app.get('/api/v1/zips/1')
        data = json.loads(rv.data)
        assert data["family_income"] == "12345"

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
        assert data["week_id"] == "1"

    def test_weeks_has_start_date(self):
        rv = self.app.get('/api/v1/weeks/1')
        data = json.loads(rv.data)
        assert data["start_date"] == "10/11/15"

    def test_weeks_has_end_date(self):
        rv = self.app.get('/api/v1/weeks/1')
        data = json.loads(rv.data)
        assert data["end_date"] == "10/17/15"

if __name__ == '__main__':
    unittest.main() 