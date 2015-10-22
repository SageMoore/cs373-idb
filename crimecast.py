from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path="")

# Homepage
@app.route('/')
def splash():
    return app.send_static_file('index.html')


# Static crimes page
@app.route('/crimes')
def crimes():
    return app.send_static_file('crimes.html')


# Static weeks page
@app.route('/weeks')
def weeks():
    return app.send_static_file('weeks.html')


# Crime Type
@app.route('/crimetype')
def crimetype_home():
    return app.send_static_file('crimeType_1.html')


@app.route('/crimetype/<crimetype_id>')
def crimetype(crimetype_id):
    print(crimetype_id)
    type_file = 'crimeType_' + str(crimetype_id) + '.html'
    print(type_file)
    return app.send_static_file(type_file)

@app.route('/zips')
def zip_home():
    return app.send_static_file('zips.html')

@app.route('/zips/<zip_id>')
def zip(zip_id):
	return app.send_static_file('zips1.html', zip_id=zip_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
