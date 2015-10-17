from flask import Flask

app = Flask(__name__, static_url_path = "")

#crimes page
@app.route('/crimes')
def crimes():
	return app.send_static_file('crimes.html')

@app.rout('/weeks')
def weeks():
    return app.send_static_file('weeks.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
