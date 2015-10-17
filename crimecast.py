from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path="")

# Homepage
@app.route('/')
def splash():
    return render_template('splash.html')


# Static crimes page
@app.route('/crimes')
def crimes():
    return render_template('crimes.html')


# Static weeks page
@app.route('/weeks')
def weeks():
    return render_template('weeks.html')


# Crime Type
@app.route('/crimetype')
def crimetype_home():
    return app.send_static_file('crimeTypes.html')


@app.route('/crimetype/<crimetype_id>')
def crimetype(crimetype_id):
    return app.send_static_file('crimeType_' + str(crimetype_id) + ' .html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
