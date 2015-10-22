import os
import crimecast
import unittest
import tempfile

from flask import json, jsonify

class CrimecastTestCase(unittest.TestCase):

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
        rv = self.app.get('/crimes')
        assert len(rv.data) > 0

    def test_crimes_has_id(self):
        rv = self.app.get('/crimes/12345')
        data = json.loads(rv.data)
        self.assert_equal(data["id"], "12345")

    def test_crimes_has_address(self):
        rv = self.app.get('/crimes/12345')
        data = json.loads(rv.data)
        self.assert_equal(data["address"], "123 Street Name Dr")

    def test_crimes_has_type(self):
        rv = self.app.get('/crimes/12345')
        data = json.loads(rv.data)
        self.assert_equal(data["crime_type"], "22222")

    def test_crimes_has_zip(self):
        rv = self.app.get('/crimes/12345')
        data = json.loads(rv.data)
        self.assert_equal(data["zipcode"], "33333")

    def test_crimes_has_date(self):
        rv = self.app.get('/crimes/12345')
        data = json.loads(rv.data)
        self.assert_equal(data["date"], "1-1-2016")

    # ----------------------
    # Crime_Types unit tests
    # ----------------------

    def test_crime_types_non_empty_response(self):
        rv = self.app.get('/crimetype')
        assert len(rv.data) > 0

    def test_crime_types_has_crimes(self):
        rv = self.app.get('/crimetype/22222')
        data = json.loads(rv.data)
        self.assert_equal(data["crimes"], [12345, 12346, 12347])

    def test_crime_types_has_title(self):
        rv = self.app.get('/crimetype/22222')
        data = json.loads(rv.data)
        self.assert_equal(data["title"], "Assault")

    def test_crime_types_has_description(self):
        rv = self.app.get('/crimetype/22222')
        data = json.loads(rv.data)
        self.assert_equal(data["description"], "Assaults are bad")

    # ---------------
    # Zips unit tests
    # ---------------

    def test_zips_non_empty_response(self):
        rv = self.app.get('/zips')
        assert len(rv.data) > 0

    def test_zips_has_id(self):
        rv = self.app.get('/zips/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["id"], "33333")

    def test_zips_has_crimes(self):
        rv = self.app.get('/zips/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["crimes"], [12345, 12346, 12347])

    def test_zips_has_zipcode(self):
        rv = self.app.get('/zips/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["zipcode"], "78705")

    def test_zips_has_lat(self):
        rv = self.app.get('/zips/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["lat"], "32.123")

    def test_zips_has_long(self):
        rv = self.app.get('/zips/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["long"], "32.123")

    # ----------------
    # Weeks unit tests
    # ----------------

    def test_weeks_non_empty_response(self):
        rv = self.app.get('/weeks')
        assert len(rv.data) > 0

    def test_zips_has_id(self):
        rv = self.app.get('/weeks/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["id"], "11111")

    def test_zips_has_crimes(self):
        rv = self.app.get('/weeks/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["crimes"], [12345, 12346, 12347])

    def test_zips_has_start_date(self):
        rv = self.app.get('/weeks/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["start_date"], "1-1-2015")

    def test_zips_has_end_date(self):
        rv = self.app.get('/weeks/33333')
        data = json.loads(rv.data)
        self.assert_equal(data["end_date"], "1-7-2015")

if __name__ == '__main__':
    unittest.main() 