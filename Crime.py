from flask.ext.restful import Resource
from CrimeList import CRIMES

__author__ = 'markdaniel'
# Crime
# returns a crime by id
class CrimeById(Resource):
    def get(self, crime_id):
        # assert len(CRIMES) > crime_id
        return CRIMES[int(crime_id) - 1]

    def post(self):
        pass