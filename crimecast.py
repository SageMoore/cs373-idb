import json
import codecs
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import subprocess, os
# from Crime import CrimeById
# import CrimeList
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import db_connect, Crime, Week, Zip, CrimeType

app = Flask(__name__, static_url_path="")
api = Api(app)

#//username:password@host:port/database

# engine = create_engine('postgres://crimedata:poop@crimecast.xyz:5000/crimedata')

# engine = create_engine('postgresql://crimedata:poop@localhost/crimedata')
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


CRIMES = [
    {
        'crime_id': '1',
        'lat': '30.28500',
        'lng': '-97.7320000',
        'address': 'GDC',
        'crime_type':
            {
                'crime_type_id': '1',
                'name': 'Vandalism'
             },
        'time': '10-12-2015 19:12:00',
        'description': 'Graffiti of pig on building',
        'zip_code':
            {
                'zip_id': '1',
                'zip_code': '78704'
            },
        'week':
            {
                'week_id': '1',
                'start_date': '10/11/15'
            }
    },
    {'crime_id': '2', 'lat': '30.30000', 'lng': '-97.730000', 'address': 'Duval Rd', 'crime_type': {'crime_type_id': '2', 'name': 'Burglary'}, 'time': '10-20-2015 19:20:00', 'description': 'Burglary at Quacks Bakery', 'zip_code': {'zip_id': '2', 'zip_code': '78705'}, 'week': {'week_id': '2', 'start_date': '10/18/15'}},
    {'crime_id': '3', 'lat': '30.27000', 'lng': '-97.7190000', 'address': '12th and Chicon', 'crime_type': {'crime_type_id': '3', 'name': 'Assault'}, 'time': '10-30-2015 22:20:00', 'description': 'Murder on 12th and Chicon', 'zip_code': {'zip_id': '3', 'zip_code': '78706'}, 'week': {'week_id': '3', 'start_date': '10/25/15'}}
]

CRIMETYPES = [
    {
        'crime_type_id': '1',
        'name': 'Vandalism',
        'desc': 'Vandalism is bad',
        'worstZip':
            {
                'zip_id': '1',
                'zip_code': '78704'
            },
        'worstWeek':
            {
                'week_id': '1',
                'start_date': '10/11/15'
            }
        , 'crimes':
        [
            {'crime_id': '1',
             'description': 'Graffiti of pig on building'}
        ]
    },
    {'crime_type_id': '2', 'name': 'Burglary', 'desc': 'Burglary is bad', 'worstZip': {'zip_id': '2', 'zip_code': '78705'}, 'worstWeek': {'week_id': '2', 'start_date': '10/18/15'}, 'crimes': [{'crime_id': '2', 'description': 'Burglary at Quacks Bakery'}, {'crime_id': '2', 'description': 'Burglary at Quacks Bakery'}, {'crime_id': '2', 'description': 'Burglary at Quacks Bakery'}]},
    {'crime_type_id': '3', 'name': 'Assault', 'desc': 'Assault is bad', 'worstZip': {'zip_id': '3', 'zip_code': '78706'}, 'worstWeek': {'week_id': '3', 'start_date': '10/25/15'}, 'crimes': [{'crime_id': '3', 'description': 'Murder on 12th and Chicon'}]},
]

ZIPS = [
        {
            'zip_id': '1',
            'zip_code': '78704',
            'lat': '30.28500',
            'lng': '-97.7320000',
            'pop': '12345',
            'family_income': '12345',
            'crimes':
                [
                    {'crime_id': '1',
                     'description': 'Graffiti of pig on building'}
                ]
        },
        {'zip_id': '2', 'zip_code': '78705', 'lat': '30.123', 'lng': '30.123', 'pop': '12345', 'family_income':'12345', 'crimes': [{'crime_id': '2', 'description': 'Burglary at Quacks Bakery'}]},
        {'zip_id': '3', 'zip_code': '78706', 'lat': '35.123', 'lng': '35.123', 'pop': '12345', 'family_income':'12345', 'crimes': [{'crime_id': '3', 'description': 'Murder on 12th and Chicon'}]}
]

WEEKS = [
        {
            'week_id': '1',
            'start_date': "10/11/15",
            'end_date': "10/17/15",
            'mostPopular': {
                'crime_type_id': '1',
                'name': 'Vandalism'
            },
            'worstZip': {
                'zip_id': '1',
                'zip_code': '78704'
            },
            'crimes':
                [
                    {'crime_id': '1',
                     'description': 'Graffiti of pig on building'}
                ]
        },
        {'week_id': '2', 'start_date': "10/18/15", 'end_date': "10/24/15", 'mostPopular': {'crime_type_id': '2', 'name': 'Burglary'}, 'worstZip': {'zip_id': '2', 'zip_code': '78705'}, 'crimes': [{'crime_id': '2', 'description': 'Burglary at Quacks Bakery'}]},
        {'week_id': '3', 'start_date': "10/25/15", 'end_date': "10/31/15", 'mostPopular': {'crime_type_id': '3', 'name': 'Assault'}, 'worstZip': {'zip_id': '3', 'zip_code': '78706'}, 'crimes': [{'crime_id': '3', 'description': 'Murder on 12th and Chicon'}]},
]


# Crimes
# shows a list of all crimes, and lets you POST to add new tasks
class CrimeList(Resource):
    def get(self):
        all_crimes = session.query(Crime).all()
        crimes_json = []
        for c in all_crimes:
            # crime_json = {'crime_id' : c.crime_id, 'lat' : c.lat, 'lng' : c.lng, 'address' : c.address, 'crime_type' : c.crime_type, 'time' : c.time, 'description' : c.description, 'zip_code' : c.zip_code, 'week' : c.week}
            crime_json = row_to_dict(c)
            crimes_json += [crime_json]
        return json.dumps(crimes_json)

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
        crime = session.query(Crime).from_statement(text("select * from crime where crime_id=:crime_id")).params(crime_id=crime_id).all()
        # crime_json = {'crime_id': crime.crime_id,
        #               'lat': crime.lat,
        #               'lng': crime.lng,
        #               'address': crime.address,
        #               'crime_type': crime.crime_type,
        #               'time': str(crime.time),
        #               'description': crime.description,
        #               'zip_code': crime.zip_code,
        #               'week': crime.week}
        crime_json = row_to_dict(crime)
        return json.dumps(crime_json)

    def post(self):
        pass

# Crime Types
# shows a list of all crime types
class CrimeTypeList(Resource):
    def get(self):
        all_crime_types = session.query(CrimeType).all()
        crime_types_json = []
        for crime_type in all_crime_types:
            worst_week = session.query(Week).from_statement(text("select * from week where week_id=:week_id")).params(week_id=crime_type.worst_week).first()
            worst_zip = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=crime_type.worst_zip).first()
            # crime_type_json = {'crime_type_id':crime_type.crime_type_id,
            #                    'name':crime_type.name,
            #                    'desc':crime_type.desc,
            #                    'worst_zip':crime_type.worst_zip,
            #                    'worst_week':crime_type.worst_week}
            crime_type_json = row_to_dict(crime_type)
            if worst_week is not None:
                crime_type_json['worst_week'] = row_to_dict(worst_week)
            if worst_zip is not None:
                crime_type_json['worst_zip'] = row_to_dict(worst_zip)
            print("all crime types", crime_type_json)
            crime_types_json += [crime_type_json]
        # return all_crime_types
        return json.dumps(crime_types_json)

    def post(self):
        pass

# Crime Type
# returns a crime type by id
class CrimeTypeById(Resource):
    def get(self, crime_type_id):
        # select * from CRIMETYPES as c where crime_id = c.id
        print("sawgawgawg",crime_type_id)
        crime_type = session.query(CrimeType).from_statement(text("select * from crime_type where crime_type_id=:crime_type_id")).params(crime_type_id=crime_type_id).first()
        print(crime_type)
        worst_week = session.query(Week).from_statement(text("select * from week where week_id=:week_id")).params(week_id=crime_type.most_popular).first()
        worst_zip = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=crime_type.worst_zip).first()
        # crime_type_json = {'crime_type_id':crime_type.crime_type_id,
        #                    'name':crime_type.name,
        #                    'desc':crime_type.desc,
        #                    'worst_zip':crime_type.worst_zip,
        #                    'worst_week':crime_type.worst_week}
        crime_type_json = row_to_dict(crime_type)
        if worst_week is not None:
            crime_type_json['worst_week'] = row_to_dict(worst_week)
        if worst_zip is not None:
            crime_type_json['worst_zip'] = row_to_dict(worst_zip)
        print("individual crime asdffdsa", crime_type_json)
        return json.dumps(crime_type_json)

    def post(self):
        pass

# Weeks
# shows a list of all weeks
class WeekList(Resource):
    def get(self):
        all_weeks = session.query(Week).all()
        # return all_weeks
        weeks_json = []
        for week in all_weeks:
            most_popular = session.query(CrimeType).from_statement(text("select * from crime_type where crime_type_id=:crime_type_id")).params(crime_type_id=week.most_popular).first()
            print("made it past popular", most_popular)
            worst_zip = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=week.worst_zip).first()
            print("made it past zip", worst_zip)
            # week_json= {'week_id':week.week_id,
            #             'start': str(week.start),
            #             'end': str(week.end),
            #             'most_popular': {
            #                 'week_id': most_popular.week_id,
            #                 'start': most_popular.start
            #             },
            #             'worst_zip':week.worst_zip}
            week_json = row_to_dict(week)
            print(week_json)
            if most_popular is not None:
                week_json['most_popular'] = row_to_dict(most_popular)
            if worst_zip is not None:
                week_json['worst_zip'] = row_to_dict(worst_zip)
            print("all weeks fdafasdda",week_json)
            weeks_json += [week_json]
        # return all weeks
        return json.dumps(weeks_json)

    def post(self):
        pass

# Week
# returns a week by id
class WeekById(Resource):
    def get(self, week_id):
        week = session.query(Week).from_statement(text("select * from week where week_id=:week_id")).params(week_id=week_id).all()
        most_popular = session.query(CrimeType).from_statement(text("select * from crime_type where crime_type_id=:crime_type_id")).params(crime_type_id=week.most_popular).first()
        worst_zip = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=week.worst_zip).first()
        # week_json= {'week_id':week.week_id,
        #             'start':str(week.start),
        #             'end':str(week.end),
        #             'most_popular':week.most_popular,
        #             'worst_zip':week.worst_zip}
        week_json = row_to_dict(week)
        if most_popular is not None:
            week_json['most_popular'] = row_to_dict(most_popular)
        if worst_zip is not None:
            week_json['worst_zip'] = row_to_dict(worst_zip)
        print("individual week asdfasdf",week_json)
        return json.dumps(week_json)
    def post(self):
        pass

# Zipcodes
# shows a list of all zipcodes
class ZipList(Resource):
    def get(self):
        # all_zips = session.query(Zip).all()
        # return all_zips
        all_zips = session.query(Zip).all()
        # return all_weeks
        zips_json = []
        for z in all_zips:
            # z_json= {'zip_id':z.zip_id,
            #          'zip_code':z.zip_code,
            #          'lat':z.lat,
            #          'lng':z.lng,
            #          'pop':z.pop,
            #          'family_income':z.family_income}
            z_json = row_to_dict(z)
            zips_json += [z_json]
        # return all weeks
        return json.dumps(zips_json)

    def post(self):
        pass

# Zipcode
# returns a zipcode by id
class ZipById(Resource):
    def get(self, zip_id):
        z = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=zip_id).all()
        # z_json= {'zip_id':z.zip_id,
        #          'zip_code':z.zip_code,
        #          'lat':z.lat,
        #          'lng':z.lng,
        #          'pop':z.pop,
        #          'family_income':z.family_income}
        z_json = row_to_dict(z)

        return json.dumps(z_json)

    def post(self):
        pass

# Helper method, converts SQLAlchemy row to a dictionary
def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

# Unit Tests
# Returns the results of running tests.py -- for use on the 'About' page
class Tests(Resource):
    def get(self):
        #p = subprocess.Popen('python cs373-idb/tests.py', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output, errors = p.communicate()
        #return { 'results': str(output) }
        #return { 'results': 'HERP DERP FLERP' }

        res = ''
        path = os.path.dirname(os.path.realpath(__file__))
        for i in run_command(('python3 ' + path + '/tests.py').split()):
            res += i.decode("utf-8")

        return { 'results': res }

def run_command(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        retcode = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break

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
