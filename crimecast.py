from flask import Flask

app = Flask(__name__, static_url_path = "")

# Homepage
@app.route('/')
def splash():
    return app.send_static_file('splash.html')

# Static crimes page
@app.route('/crimes')
def crimes():
	return app.send_static_file('crimes.html')

# Static weeks page
@app.route('/weeks')
def weeks():
    return app.send_static_file('weeks.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
