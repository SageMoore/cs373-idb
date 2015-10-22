import urllib, json, sys

def fetch_data(lat, lng):
	response = urllib.urlopen('http://api.spotcrime.com/crimes.json?lat=' + str(lat) + '&lon=' + str(lng) + '&radius=0.02&key=spotcrime-private-api-key')
	data = json.loads(response.read())
	return data

def write_data(min_lat, max_lat, min_lng, max_lng):
	crime_list = []
	number_keys = ['cdid', 'lon', 'lat']
	target = open('daily_spot_crime_data.json', 'w')
	# necessary to write manually due to formatting issue
	target.write("{\"crimes\": [")
	first_crime = True

	while min_lat < max_lat:
		lng = min_lng
		while lng < max_lng:
			page_data = fetch_data(min_lat, lng)
			for crime in page_data['crimes']:
				if not crime in crime_list:
					if first_crime:
						first_crime = False
					else:
						target.write(",")
					target.write("{")
					crime_len = len(crime)
					for key in crime:
						target.write("\"" + key + "\":")
						if key in number_keys:
							target.write(str(crime[key]))
						else:
							target.write("\"" + str(crime[key]) + "\"")
						if crime_len > 1:
							target.write(",")
						crime_len -= 1
					crime_list.append(crime)
					target.write("}")	
			lng += .015 #increase by .015 to make sure we get all the data
		min_lat += .015 #increase by .015 to make sure we get all the data
	target.write("]}")

if __name__ == '__main__':
	min_lat = 30.222428
	max_lat = 30.349176
	min_lng = -97.820206
	max_lng = -97.653351
	write_data(min_lat, max_lat, min_lng, max_lng)