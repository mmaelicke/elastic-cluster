from faker import Faker
from random import choice,choices, randint
from datetime import datetime as dt
import json
import requests

f = Faker('de_DE')

variables = [
	'air temperature',
	'relative humidity',
	'air pressure',
	'soil moisture',
	'sap flow',
	'water level',
	'wind direction',
	'wind speed',
	'rainfall',
	'snow height',
	'turbidity'
]

title_words = [
	'long', 'term', 'Southern', 'Cluster', 'unique', 'generic', 'lab', 'recession', 'Germany',
	'global', 'climate', 'change', 'integrated'
]

licenses = [
	'CC Zero 1.0', 'CC BY 3.0', 'CC BY-SA 4.0', 'CC BY-SA-NC 4.0'
]

names = [f.name() for _ in range(10)]

def entry():
	v = choice(variables)
	entry = dict(
		title=choice(title_words) + ' ' + v + ' ' + ' '.join([choice(title_words) for _ in range(2)]),
		variable=v,
		license=choice(licenses),
		attribution=f.catch_phrase() + ' by ' + f.name(),
		owner=choice(names),
		description=' '.join([choice([f.catch_phrase(), f.city(), f.address(), choice(variables), choice(title_words)]) for _ in range(randint(3, 8))]),
		created=dt.now().isoformat(),
		edited=dt.now().isoformat()
	)
	s = dict(
		address=f.address(),
		mail=f.email(),
		sensor=f.company() + '' + f.company_suffix() + ' ' + choice(variables),
		url=f.uri(),
		datasheet=f.file_path(),
		height=randint(600, 20000) / 10.,
		landuse=choice(['forest', 'pasture', 'urban', 'agriculture', 'weed']),
		medium=choice(['ground', 'soil', 'water', 'air', 'athmosphere', 'rhizosphere', 'pedosphere'])
	)
	entry['supplementary'] = {k:s[k] for k in choices(list(s.keys()), k=6)}
	return entry


def upload(index_name, N=500, url='http://localhost:9200/_bulk'):
	action = json.dumps({'index':{'_index': index_name, '_type':'page'}})
	data = ''
	for i in range(N):
		if i == 500:
			break
		data += action + '\n'
		data += json.dumps(entry()) + '\n'
	
	response = requests.post(url, data=data, headers={'content-type':'application/json'})
	print('[%d] Sending bulk of 500...' % (i / 500 + 1))
	r = json.loads(response.content)	
	print('[%s] Took %d ms.' %('FINISHED' if not r['errors'] else 'FAILED', r['took'])  )
	# check if sending is finished	
	if N > 500:
		upload(index_name, N=N - 500, url=url)


if __name__=='__main__':
	import json
	print(json.dumps(entry(), indent=4))
