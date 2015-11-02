from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
# from Crime import CrimeById
# import CrimeList

app = Flask(__name__, static_url_path="")
api = Api(app)

parser = reqparse.RequestParser()
# parser.add_argument('crime')

# Homepage
@app.route('/')
@app.route('/splash')
def splash():
    return app.send_static_file('index.html')

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return app.send_static_file('index.html')

# Static crimes page
@app.route('/crimes')
def crimes():
    return app.send_static_file('index.html')

# Static crime page
@app.route('/crime/<crime_id>')
def crime(crime_id):
    return app.send_static_file('index.html')


# Static weeks page
@app.route('/weeks')
def weeks():
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

# Crime
# returns a crime by id
class CrimeById(Resource):
    def get(self, crime_id):
        # assert len(CRIMES) > crime_id
        return CRIMES[int(crime_id) - 1]

    def post(self):
        pass

# Unit Tests
# Returns the results of running tests.py -- for use on the 'About' page
class Tests(Resource):
    def get(self):
        tests_proc = subprocess.Popen(['python', 'tests.py'], 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return tests_proc.communicate()[0]

##
## Actually setup the Api resource routing here
##
api.add_resource(CrimeList, '/api/v1/crimes')
api.add_resource(CrimeById, '/api/v1/crime/<crime_id>')
api.add_resource(Tests, '/api/v1/tests')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
