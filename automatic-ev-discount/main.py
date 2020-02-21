import requests
import os
import schedule
import time
import json
from requests.auth import HTTPBasicAuth

threshold = int(os.environ['THRESHOLD'])
interval = int(os.environ['INTERVAL'])
discount = int(os.environ['DISCOUNT'])
discounted = False

print('Concurrently checking PV Production...')
print("Threshold defined: {}".format(threshold))
print("Checking PV production with {} minutes of interval.".format(interval))


def checkPVPeakProduction():
    print("Checking the production peak...")
    global discounted
    r = requests.get('http://gateway:8181/api/objects/f0467701-f16c-4eba-b484-4119fdc79230/properties/W1-P1', auth=HTTPBasicAuth('714663d0-e312-4e46-a859-11141b219e82', 'KlL2PXWPqpEIbxU+rUjbVpzE7xGJTeJIDFaJOXvgEMA='))
    r = r.json()

    print("Observed value for production peak: {}".format(r['message'][0]['observed-value']))

    if r['message'][0]['observed-value'] > threshold and discounted == False:
        print("Production peak at {}! Set discount of {}%!".format(r['message'][0]['observed-value'], discount))
        requests.patch('http://msp:9998/providers/10/discount', data=json.dumps({'discount_rate':discount}))
        discounted = True

    elif r['message'][0]['observed-value'] <= threshold and discounted == True:
        print("Production peak bellow threshold! Set discount 0%!")
        requests.patch('http://msp:9998/providers/10/discount', data=json.dumps({'discount_rate':0}))
        discounted = False
    else:
        print("No change required.")




checkPVPeakProduction()
schedule.every(interval).minutes.do(checkPVPeakProduction)

while 1:
    schedule.run_pending()
    time.sleep(1)
