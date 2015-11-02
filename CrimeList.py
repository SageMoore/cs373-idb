# from flask.views import MethodView
from flask.ext.restful import Resource
from flask_restful import reqparse
from crimecast import parser

__author__ = 'markdaniel'

# parser = reqparse.RequestParser()

CRIMES = [
    { 'id': 1, 'description': "Graffiti of pig on building", 'time': "10-20-2015 19:12:00" ,'address': "GDC", 'crime_type' : 'Vandalism', 'lat' : 30.28500, 'lng' : -97.7320000  },
    { 'id': 2, 'description': "Burglary at Quacks Bakery", 'time': "10-20-2015 19:20:00" ,'address': "Duval Rd", 'crime_type' : 'Burglary', 'lat' : 30.30000, 'lng' : -97.730000  },
    { 'id': 3, 'description': "Murder on 12th and Chicon", 'time': "10-20-2015 22:20:00" ,'address': "12th and Chicon", 'crime_type' : 'Murder', 'lat' : 30.27000, 'lng' : -97.7190000  }
]

# Crimes
# shows a list of all crimes, and lets you POST to add new tasks
class CrimeList(Resource):
    def get(self):
        return CRIMES

    def post(self):
        args = parser.parse_args()
        crime_id = int(max(CRIMES.keys()).lstrip('crime')) + 1
        crime_id = 'crime%i' % crime_id
        CRIMES[crime_id] = {'crime': args['crime']}
        return CRIMES[crime_id], 201