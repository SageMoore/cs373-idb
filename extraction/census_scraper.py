import requests
import json

api_key = "b7f9ab9a5bf8671bd4207228e29abebd03418b70"

zip_codes = [78610, 78613, 78617, 78641, 78652, 78653, 78660, 78664, 78681, 78701, 78702, 78703, 78704, 78705,\
            78712, 78717, 78719, 78721, 78722, 78723, 78724, 78725, 78726, 78727, 78728, 78729, 78730, 78731, \
            78732, 78733, 78734, 78735, 78736, 78737, 78738, 78739, 78741, 78742, 78744, 78745, 78746, 78747, \
            78748, 78749, 78750, 78751, 78752, 78753, 78754, 78756, 78757, 78758, 78759]

params = {'B00001': 'Total Population',
          'B02001': 'Race',
          'B01001': 'Sex by Age',
          'B11001': 'Household Type',
          'B17020': 'Poverty Status by age',
          'B19001': 'Household Income',
          'B19101': 'Family Income',
          'B19301': 'Per Capita Income',
          'B25002': 'Occupancy Status',
          'B25003': 'Tenure',
          'B25061': 'Rent Asked',
          'B25075': 'Value for owner-occupied units',
          'B25085': 'Price Asked (for house?)',
          'B25104': 'Monthly housing cost'
          }

if __name__ == "__main__":
    variables = open('census_variables.json')
    all_params = json.load(variables)
    all_results = {z: {} for z in zip_codes}

    for param in all_params['variables']:
        if '_' in param and param[:param.index('_')] in params and not param.endswith('M'):
            print("getting information for", param)
            for zip_code in zip_codes:
                api_params = {'get': 'NAME,' + param,
                              'for': 'zip code tabulation area:'+str(zip_code),
                              'key': api_key}
                r = requests.get("http://api.census.gov/data/2013/acs5", params=api_params)
                data = r.json()
                itr = iter(data)
                keys = next(itr)
                values = [dict(zip(keys, vals)) for vals in itr]
                for value in values:
                    value['description'] = all_params['variables'][param]['label']
                all_results[zip_code][param] = values

    with open('zip_data.out', 'w') as outfile:
        json.dump(all_results, outfile)
