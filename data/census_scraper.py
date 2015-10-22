import requests

api_key = "b7f9ab9a5bf8671bd4207228e29abebd03418b70"

zip_codes = [78610, 78613, 78617, 78641, 78652, 78653, 78660, 78664, 78681, 78701, 78702, 78703, 78704, 78705,\
            78712, 78717, 78719, 78721, 78722, 78723, 78724, 78725, 78726, 78727, 78728, 78729, 78730, 78731, \
            78732, 78733, 78734, 78735, 78736, 78737, 78738, 78739, 78741, 78742, 78744, 78745, 78746, 78747, \
            78748, 78749, 78750, 78751, 78752, 78753, 78754, 78756, 78757, 78758, 78759]

if __name__ == "__main__":
    print("getting information from census")
    for zip_code in zip_codes:
        api_params = {'get': 'NAME,B01001_001E', 'for': 'zip code tabulation area:'+str(zip_code), 'key': api_key}
        r = requests.get("http://api.census.gov/data/2013/acs5", params=api_params)
        data = r.json()
        itr = iter(data)
        keys = next(itr)
        values = (dict(zip(keys, vals)) for vals in itr)
        values = list(values)
        print("Zipcode", zip_code, "Population", int(values[0]['B01001_001E']))
