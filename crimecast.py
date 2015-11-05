from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import subprocess
# from Crime import CrimeById
# import CrimeList
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db_connect, Crime, Week, Zip, CrimeType

app = Flask(__name__, static_url_path="")
api = Api(app)

#//username:password@host:port/database

# engine = create_engine('postgres://crimedata:poop@crimecast.xyz:5000/crimedata')
engine = db_connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Query a specific table in database example
#result = engine.execute("select latitude from zipcode")

#convert rows to dictionary
#my_dict = {}
#for row in result:
#go through the columns and add to the dictionary
#    d["latitude"] = row['latitude']
#    print "latitude:", row['latitude']

#convert dictionary to json
#json.dumps(my_dict)




parser = reqparse.RequestParser()
# parser.add_argument('crime')

# Homepage
@app.route('/')
@app.route('/splash')
def splash():
    print('in splash')
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    print('in default')
    return app.send_static_file('index.html')

# Static crimes page
@app.route('/crimes')
def crimes():
    return app.send_static_file('index.html')

# Static crime page
@app.route('/crimes/<crime_id>')
def crime(crime_id):
    return app.send_static_file('index.html')


# Static weeks page
@app.route('/weeks')
def weeks():
    return app.send_static_file('index.html')

# Static week page
@app.route('/weeks/<week_id>')
def week(week_id):
    return app.send_static_file('index.html')


# Crime Type
@app.route('/crime_types')
def crimetype_home():
    return app.send_static_file('index.html')

@app.route('/crime_types/<crimetype_id>')
def crimetype(crimetype_id):
    print(crimetype_id)
    type_file = 'crimeType_' + str(crimetype_id) + '.html'
    print(type_file)
    return app.send_static_file(type_file)

@app.route('/zips')
def zip_home():
    return app.send_static_file('index.html')

@app.route('/zips/<zip_id>')
def zip(zip_id):
	return app.send_static_file('zips1.html', zip_id=zip_id)

@app.route('/about')
def about():
    return app.send_static_file('index.html')


CRIMES = [
    { 'id': 1, 'description': "Graffiti of pig on building", 'time': "10-20-2015 19:12:00" ,'address': "GDC", 'crime_type' : {'crime_type_id' : 3, 'crime_type_name' : 'Vandalism'}, 'lat' : 30.28500, 'lng' : -97.7320000  },
    { 'id': 2, 'description': "Burglary at Quacks Bakery", 'time': "10-20-2015 19:20:00" ,'address': "Duval Rd", 'crime_type' : {'crime_type_id' : 2, 'crime_type_name' : 'Burglary'}, 'lat' : 30.30000, 'lng' : -97.730000  },
    { 'id': 3, 'description': "Murder on 12th and Chicon", 'time': "10-20-2015 22:20:00" ,'address': "12th and Chicon", 'crime_type' : {'crime_type_id' : 1, 'crime_type_name' : 'Assault'}, 'lat' : 30.27000, 'lng' : -97.7190000  }
]

CRIMETYPES = [
    {'id': 2, 'crime_type': 'Burglary', 'description': "Burglary is bad", "crimes": [{"id": 2},{"id": 2},{"id": 2}], 'worst_zipcode': "78705"},
    {'id': 1, 'crime_type': 'Assault', 'description': "Assault is bad", "crimes": [{"id": 3}], 'worst_zipcode': "78704"},
    {'id': 3, 'crime_type': 'Vandalism', 'description': "Vandalism is bad", "crimes": [{"id": 1}], 'worst_zipcode': "78706"}
]

ZIPS = [
        {'id': 1, 'zipcode': 78704, 'latitude': 32.123, 'longitude': 32.123, "crimes": [{"id": 1}]},
        {'id': 2, 'zipcode': 78705, 'latitude': 30.123, 'longitude': 30.123, "crimes": [{"id": 2}]},
        {'id': 3, 'zipcode': 78706, 'latitude': 35.123, 'longitude': 35.123, "crimes": [{"id": 3}]}
]

WEEKS = [
        {'id': 1, 'start_date': "10/11/15", 'end_date': "10/17/15", 'popular_crime': "1", "crimes": [{"id": 1}]},
        {'id': 2, 'start_date': "10/18/15", 'end_date': "10/24/15", 'popular_crime': "2", "crimes": [{"id": 2}]},
        {'id': 3, 'start_date': "10/25/15", 'end_date': "10/31/15", 'popular_crime': "3", "crimes": [{"id": 3}]},
]

# TODO: add ur own fake data!

# Crimes
# shows a list of all crimes, and lets you POST to add new tasks
class CrimeList(Resource):
    def get(self):
        all_crimes = session.query(Crime).all()
        return all_crimes
        # return CRIMES

    def post(self):
        args = parser.parse_args()
        crime_id = int(max(CRIMES.keys()).lstrip('crime')) + 1
        crime_id = 'crime%i' % crime_id
        CRIMES[crime_id] = {'crime': args['crime']}
        return CRIMES[crime_id], 201

# Crime
# returns a crime by id
class CrimeById(Resource):
    def get(self, crime_id):
        # assert len(CRIMES) > crime_id
        return CRIMES[int(crime_id) - 1]

    def post(self):
        pass

# Crime Types
# shows a list of all crime types
class CrimeTypeList(Resource):
    def get(self):
        # all_crime_types = session.query(CrimeType).all()
        # return all_crime_types
        return CRIMETYPES

    def post(self):
        pass

# Crime Type
# returns a crime type by id
class CrimeTypeById(Resource):
    def get(self, crime_type_id):
        # select * from CRIMETYPES as c where crime_id = c.id
        return CRIMETYPES[int(crime_type_id) - 1]

    def post(self):
        pass

# Weeks
# shows a list of all weeks
class WeekList(Resource):
    def get(self):
        # all_weeks = session.query(Week).all()
        # return all_weeks
        return WEEKS

    def post(self):
        pass

# Week
# returns a week by id
class WeekById(Resource):
    def get(self, week_id):
        return WEEKS[int(week_id) - 1]

    def post(self):
        pass

# Zipcodes
# shows a list of all zipcodes
class ZipList(Resource):
    def get(self):
        # all_zips = session.query(Zip).all()
        # return all_zips
        return ZIPS

    def post(self):
        pass

# Zipcode
# returns a zipcode by id
class ZipById(Resource):
    def get(self, week_id):
        return ZIPS[int(week_id) - 1]

    def post(self):
        pass


# Unit Tests
# Returns the results of running tests.py -- for use on the 'About' page
class Tests(Resource):
    def get(self):
        p = subprocess.Popen('python tests.py', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = p.communicate()
        return { 'results': str(errors) }

##
## Actually setup the Api resource routing here
##
api.add_resource(CrimeList, '/api/v1/crimes')
api.add_resource(CrimeById, '/api/v1/crimes/<crime_id>')
api.add_resource(CrimeTypeList, '/api/v1/crime_types')
api.add_resource(CrimeTypeById, '/api/v1/crime_types/<crime_type_id>')
api.add_resource(WeekList, '/api/v1/weeks')
api.add_resource(WeekById, '/api/v1/weeks/<week_id>')
api.add_resource(ZipList, '/api/v1/zips')
api.add_resource(ZipById, '/api/v1/zips/<zip_id>')

api.add_resource(Tests, '/api/v1/tests')
api.init_app(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
