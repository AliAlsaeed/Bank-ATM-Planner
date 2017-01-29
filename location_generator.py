import requests
import json
import geocoder
import multiprocessing as mp
import time
from progressbar import ProgressBar

fn = 'part1_result.csv'
apiKey = '7273b6bfa6507f581b54f869d8334397'
customer_url = 'http://api.reimaginebanking.com/enterprise/customers?key={}'.format(apiKey)
coordinate_url = 'http://nominatim.openstreetmap.org/search/{}?format=json&polygon=1&addressdetails=0&limit=1'
atm_url = 'http://api.reimaginebanking.com/atms?lat={}&lng={}&rad={}&key={}'
start = 0
step = 1000
pbar = ProgressBar(maxval=step).start()

def listener(q):
	'''listens for messages on the q, writes to file. '''
	f = open(fn, 'wb') 
	while 1:
		m = q.get()
		if m == 'kill':
			break
		f.write(str(m) + '\n')
		f.flush()
	f.close()

def worker(customer, progress, q):
	# print(customer)
	street_number = ''
	street_name = ''
	zip_code = ''
	address_json = customer['address']
	if (address_json.has_key('street_number')):
		street_number = address_json['street_number']
	if (address_json.has_key('street_name')):
		street_name = address_json['street_name']
	if (address_json.has_key('zip')):
		zip_code = address_json['zip']

	address = str(street_number) + " " + str(street_name) + "," + str(zip_code)
	# print(address)
	geolocator = geocoder.here(address, app_id='MMeAf5MOWL10umS0JVpJ', app_code='m_zv6umczg1-1MiUKsAgWw')
	# print(geolocator)
	if (geolocator and len(geolocator.latlng) == 2):
		atm_request = atm_url.format(geolocator.latlng[0], geolocator.latlng[1], '10', apiKey)
		response = requests.get( 
			atm_request,
			headers={'content-type':'application/json'},
		)
		# print(response)
		# print(str(geolocator.latlng[0]) + ',' + str(geolocator.latlng[1]) + '\n')
		if (response.status_code == 200):
			content = json.loads(response.content)
			# print(response.content)
			if (type(content) is dict and content.has_key('data') and len(content['data']) == 0):
				# print(len(content['data']))
				# print(str(geolocator.latlng[0]) + ',' + str(geolocator.latlng[1]) + '\n')
				q.put(str(geolocator.latlng[0]) + ',' + str(geolocator.latlng[1]) + '\n')
				return str(geolocator.latlng[0]) + ',' + str(geolocator.latlng[1]) + '\n'

	pbar.update(progress)

def main():
    #must use Manager queue here, or will not work
	manager = mp.Manager()
	q = manager.Queue()    
	pool = mp.Pool(mp.cpu_count() * 2)

    #put listener to work first
	watcher = pool.apply_async(listener, (q,))

    #fire off workers
	jobs = []
    # Create a Savings Account
	response = requests.get( 
		customer_url,
		headers={'content-type':'application/json'},
	)

	counter = 0
	progress = 0
	if response.status_code == 200:
		content = json.loads(response.content)['results']
		# print(len(content))
		for i in range(start, start+step):
			customer = content[i]
			counter = counter + 1
			progress = progress + 1
			job = pool.apply_async(worker, (customer, progress, q))
			jobs.append(job)
			if (counter % 50 == 0):
				time.sleep(1)
				# print(counter)

    # collect results from the workers through the pool result queue

	for job in jobs: 
		job.get()

	pbar.finish()

    #now we are done, kill the listener
	q.put('kill')
	pool.close()

if __name__ == "__main__":
	main()
