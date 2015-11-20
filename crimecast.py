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
import urllib.request
# import requests

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
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')


# Crimes
# shows a list of all crimes, and lets you POST to add new tasks
class CrimeList(Resource):
    def get(self):
        all_crimes = session.query(Crime).all()
        crimes_json = []
        for c in all_crimes:
            # crime_json = {'crime_id' : c.crime_id, 'lat' : c.lat, 'lng' : c.lng, 'address' : c.address, 'crime_type' : c.crime_type, 'time' : c.time, 'description' : c.description, 'zip_code' : c.zip_code, 'week' : c.week}
            week = session.query(Week).from_statement(text("select * from week where week_id=:week_id")).params(week_id=c.week).first()
            zip_code = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=c.zip_code).first()
            crime_type = session.query(CrimeType).from_statement(text("select * from crime_type where crime_type_id=:crime_type_id")).params(crime_type_id=c.crime_type).first()
            crime_json = row_to_dict(c)
            if week is not None:
                crime_json['week'] = row_to_dict(week)
            if zip_code is not None:
                crime_json['zip_code'] = row_to_dict(zip_code)
            if crime_type is not None:
                crime_json['crime_type'] = row_to_dict(crime_type)
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
        crime = session.query(Crime).from_statement(text("select * from crime where crime_id=:crime_id")).params(crime_id=crime_id).first()
        week = session.query(Week).from_statement(text("select * from week where week_id=:week_id")).params(week_id=crime.week).first()
        zip_code = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=crime.zip_code).first()
        crime_type = session.query(CrimeType).from_statement(text("select * from crime_type where crime_type_id=:crime_type_id")).params(crime_type_id=crime.crime_type).first()
        crime_json = row_to_dict(crime)
        if week is not None:
            crime_json['week'] = row_to_dict(week)
        if zip_code is not None:
            crime_json['zip_code'] = row_to_dict(zip_code)
        if crime_type is not None:
            crime_json['crime_type'] = row_to_dict(crime_type)
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
            crime_type_json = row_to_dict(crime_type)
            if worst_week is not None:
                crime_type_json['worst_week'] = row_to_dict(worst_week)
            if worst_zip is not None:
                crime_type_json['worst_zip'] = row_to_dict(worst_zip)
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
        crime_type = session.query(CrimeType).from_statement(text("select * from crime_type where crime_type_id=:crime_type_id")).params(crime_type_id=crime_type_id).first()
        worst_week = session.query(Week).from_statement(text("select * from week where week_id=:week_id")).params(week_id=crime_type.worst_week).first()
        worst_zip = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=crime_type.worst_zip).first()
        crimes = []
        crimes = session.query(Crime).from_statement(text("select * from crime where crime_type=:crime_type")).params(crime_type=crime_type_id).all()
        crime_type_json = row_to_dict(crime_type)
        if worst_week is not None:
            crime_type_json['worst_week'] = row_to_dict(worst_week)
        if worst_zip is not None:
            crime_type_json['worst_zip'] = row_to_dict(worst_zip)
        if crimes is not None:
            crimes_list = []
            for crime in crimes:
                crimes_list.append(row_to_dict(crime))
            crime_type_json['crimes'] = crimes_list
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
            worst_zip = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=week.worst_zip).first()
            week_json = row_to_dict(week)
            if most_popular is not None:
                week_json['most_popular'] = row_to_dict(most_popular)
            if worst_zip is not None:
                week_json['worst_zip'] = row_to_dict(worst_zip)
            weeks_json += [week_json]
        # return all weeks
        return json.dumps(weeks_json)

    def post(self):
        pass

# Week
# returns a week by id
class WeekById(Resource):
    def get(self, week_id):
        week = session.query(Week).from_statement(text("select * from week where week_id=:week_id")).params(week_id=week_id).first()
        most_popular = session.query(CrimeType).from_statement(text("select * from crime_type where crime_type_id=:crime_type_id")).params(crime_type_id=week.most_popular).first()
        worst_zip = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=week.worst_zip).first()
        crimes = []
        crimes += session.query(Crime).from_statement(text("select * from crime where week=:week_id")).params(week_id=week_id).all()
        week_json = row_to_dict(week)
        if most_popular is not None:
            week_json['most_popular'] = row_to_dict(most_popular)
        if worst_zip is not None:
            week_json['worst_zip'] = row_to_dict(worst_zip)
        if crimes is not None:
            crimes_list = []
            for crime in crimes:
                crimes_list.append(row_to_dict(crime))
            week_json['crimes'] = crimes_list
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
        z = session.query(Zip).from_statement(text("select * from zip where zip_id=:zip_id")).params(zip_id=zip_id).first()
        crimes = []
        crimes += session.query(Crime).from_statement(text("select * from crime where zip_code=:zip_id")).params(zip_id=zip_id).all()
        z_json = row_to_dict(z)
        if crimes is not None:
            crimes_list = []
            for crime in crimes:
                crimes_list.append(row_to_dict(crime))
            z_json['crimes'] = crimes_list
        return json.dumps(z_json)

    def post(self):
        pass

# Cars
# returns a list of cars
class CarList(Resource):
    def get(self):
        print('in carslist....ccc')
        request = 'http://162.242.248.195/model_api'
        # r = requests.get(request)
        # print('got r')
        # data = r.json()
        print(str(data))
        # print('for request: ' + request)
        # urlopen = urllib.request.urlopen(request)
        # print('url opened')
        # print(urlopen)
        # data = json.loads(urlopen)
        # response = urllib.request.urlopen(request)
        # print(str(response.data))
        # try:
        #     obj = json.load(response)
        #     print(obj)
        #     str_response = response.readall().decode('utf-8')
        #     data = json.loads(str_response)
        #     print('attempt to get data successful')
        # except Exception as e:
        #     print('something went wrong')
        #     print(e)
        #
        # print(str(data))
        print('got the data')
        # print(json.dumps(data))
        return 'hello'

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
        for i in run_command(('make crimecast-test.tmp').split()):
            res += i.decode("utf-8")
#        for i in run_command(('coverage3 run --branch ' + path + '/tests.py 2>&1').split()):
#            res += i.decode("utf-8")
#        for i in run_command(('coverage3 report -m').split()):
#            res += i.decode("utf-8")

        return json.dumps({ 'results': res })

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
api.add_resource(CarList, '/api/v1/carlist')
api.init_app(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
