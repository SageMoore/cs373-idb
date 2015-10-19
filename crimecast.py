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
    return render_template('crimeType_1.html')


@app.route('/crimetype/<crimetype_id>')
def crimetype(crimetype_id):
    print(crimetype_id)
    type_file = 'crimeType_' + str(crimetype_id) + '.html'
    print(type_file)
    return render_template(type_file)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
