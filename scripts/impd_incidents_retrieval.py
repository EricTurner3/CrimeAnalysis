import requests
import json
import time
import csv
import pandas as pd

'''
IMPD stores incident data in CityProtect. They allow bulk csv downloads, however doing it this way omits Geospatial data

Instead I wrote this script to extract the data from the live webapp which includes latitude and longitude coords for use in
GIS software

API Endpoint and request found from Developer Tools, passed into Postman and copied starter code

Eric Turner
6 Oct 2021
'''
# for saving the data to file
def save(incidents):
    for i in incidents: 
        data = [i['id'], i['ccn'], i['crapiId'], i['agencyId'], i['date'], i['createDate'], i['updateDate'], i['city'], i['state'], i['location']['coordinates'][1], i['location']['coordinates'][0], i['blockizedAddress'], i['incidentType'], i['parentIncidentType'], i['narrative']]
        file.writerow(data)

# set the variables here
agency_id = "109542" # IMPD
from_date = "2021-09-01T00:00:00.000Z"
to_date = "2021-10-06T23:59:59.999Z"

print('Fetching data from CityProtect API from {} to {}'.format(from_date, to_date))

# set the initial parameters
url = "https://ce-portal-service.commandcentral.com/api/v1.0/public/incidents"
# note the limit 2000, offset 0 indicates we have pages
payload="{\"limit\":2000,\"offset\":0,\"geoJson\":{\"type\":\"Polygon\",\"coordinates\":[[[-85.95244823656743, 39.63859810688616],[-86.32601887766806, 39.63234728987109],[-86.32660942836364, 39.924062921780205],[-85.95807200939956, 39.92752525955417],[-85.95244823656743, 39.63859810688616]]]},\"projection\":false,\"propertyMap\":{\"toDate\":\""+to_date+"\",\"fromDate\":\""+from_date+"\",\"pageSize\":\"2000\",\"parentIncidentTypeIds\":\"149,150,148,8,97,104,165,98,100,179,178,180,101,99,103,163,168,166,12,161,14,16,15\",\"zoomLevel\":\"11\",\"latitude\":\"39.7800137959678\",\"longitude\":\"-86.13386541141675\",\"days\":\"1,2,3,4,5,6,7\",\"startHour\":\"0\",\"endHour\":\"24\",\"timezone\":\"+00:00\",\"relativeDate\":\"custom\",\"agencyIds\":\""+agency_id+"\"}}"
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)

# once we have the response, turn it into json
j = json.loads(response.text)

# next open a file to write out
filename = '../data/impd_incidents_'+from_date+'_'+to_date+'.csv'
output = open(filename, 'w')
file = csv.writer(output)
# we only want some of the fields
col_names = ['id', 'ccn', 'crapiId', 'agencyId', 'date', 'createDate', 'updateDate', 'city', 'state', 'lat', 'lng', 'address', 'incidentType', 'parentIncidentType', 'narrative'] 
# output that to file
file.writerow(col_names)
# save first incidents to list
incidents = j['result']['list']['incidents']
# enumerate and save to file
save(incidents)
# counters
cnt = len(incidents)
total_cnt = cnt
pg = 2

# loop to grab all the incidents
while cnt > 0:
    time.sleep(0.2) # sleep for 200ms to prevent DDOS of large requests
    # the API is nice enough to auto generate the next available payload
    payload = j['navigation']['nextPagePath']['requestData']
    print('Fetching Page {}: Limit {}, Offset {}'.format(pg, payload['limit'], payload['offset']))
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    j = json.loads(response.text)
    # append the new data
    incidents = j['result']['list']['incidents']
    save(incidents)
    # update incrementers
    pg += 1
    cnt = len(incidents)
    total_cnt += cnt

print('Total Incidents Retrieved: {}'.format(total_cnt))

output.close()

# I noticed that pulling from the API, different pages can have duplicates. Let's remove them
print('Re-opening file to check for duplicates...')
df = pd.read_csv(filename)
og = len(df.index)
df = df.drop_duplicates(subset='id', keep="first") # the uuid is unique so remove any duplicates
new = len(df.index)
df.to_csv(filename, index=False) # overwrite the original file
print('Removed {} duplicate records'.format(og-new))
print('{} incidents re-saved as ./{}'.format(new, filename))
