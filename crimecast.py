from flask import Flask

app = Flask(__name__)

#crimes page
@app.route('/crimes')
def splash():
	return app.send_static_file('crimes.html')


if __name__ == "__main__":
    app.run()