import json
import sys

if len(sys.argv) > 1:
	resource = sys.argv[1]
else:
	resource = 'houses'

with open("./{}.json".format(resource), 'r') as fd:
	data = "".join(fd.readlines())
	fd.close()

resources = json.loads(data)

for r in resources:
	print('\nTitle: ', r['title'])
	if 'price' in r:
		print('Price: ', r['price'])
	if 'post_dt' in r:
		print('Posted: ', r['post_dt'])
	if 'info' in r:
		print('Addtl info: ', r['info'])
	if 'bedrooms' in r:
		print('Bedrooms: ', r['bedrooms'])
	if 'bathrooms' in r:
		print('Bathrooms: ', r['bathrooms'])
	if 'sqft' in r:
		print('Sqft: ', r['sqft'])
	if 'dogs' in r:
		print('Dogs: ', r['dogs'])
	if 'cats' in r:
		print('Cats: ', r['cats'])
	if 'available' in r:
		print('Available: ', r['available'])
	if 'smoking' in r:
		print('Smoking: ', r['smoking'])
	if 'factoids' in r:
		print('Factoids: ', r['factoids'])
	if 'description' in r:
		print('Description: ', r['description'])
