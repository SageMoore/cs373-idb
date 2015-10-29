from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask import render_template

app = Flask(__name__, static_url_path="")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('crime')

# CRIMES = {
#     'crime1': {'crime': 'Burglary at Quacks'},
#     'crime2': {'crime': 'Vandalism at GDC'},
#     'crime3': {'crime': 'Murder at 12th and Chicon'},
# }

CRIMES = [
    { 'id': 1, 'description': "Graffiti of pig on building", 'time': "10-20-2015 19:12:00" ,'address': "GDC", 'crime_type' : 3  },
    { 'id': 2, 'description': "Burglary at Quacks Bakery", 'time': "10-20-2015 19:20:00" ,'address': "Duval Rd", 'crime_type' : 2  },
    { 'id': 3, 'description': "Murder on 12th and Chicon", 'time': "10-20-2015 22:20:00" ,'address': "12th and Chicon", 'crime_type' : 1  }
]


# Homepage
@app.route('/')
@app.route('/splash')
def splash():
    return app.send_static_file('index.html')

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index():
    return app.send_static_file('index.html')

# Static crimes page
@app.route('/crimes')
def crimes():
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


#todo: move to other files
# Crime
# returns a crime by id
class Crime(Resource):
    def get(self):
        pass #todo later

    def post(self):
        pass

# Crimes
# shows a list of all crimes, and lets you POST to add new tasks
class Crime(Resource):
    def get(self):
        return CRIMES

    def post(self):
        args = parser.parse_args()
        crime_id = int(max(CRIMES.keys()).lstrip('crime')) + 1
        crime_id = 'crime%i' % crime_id
        CRIMES[crime_id] = {'crime': args['crime']}
        return CRIMES[crime_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(Crime, '/api/v1/crimes')
# api.add_resource(Crime, '/api/v1/crimes/<crime_id>')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
