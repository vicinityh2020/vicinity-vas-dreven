# vicinity-vas-dreven
## Requirements
Install docker, docker-compose and maven
## How to run
1. Create a vicinity access point in neighbourhood manager.
2. Edit `vicinity-vas-dreven/ev-charger---device-/config/agent/config-1.json`. Change the `agent-id` and `password` in the `credentials` to reflect the ones created in step
3. In `vicinity-vas-dreven/` execute: `docker-compose up -d postgres adapter agent gateway`
4. Go to neighbourhood manager and enable the EVCharger-1 and OCPP
4.1. Make GET request to http://**host**:9997/agent/configuration to retrive Vicinity Oids and Pws
5. Edit `vicinity-vas-dreven/end-user-api---service/src/main/resources/application.properties`
5.1. The properties **gateway.auth.user** should have the OCPP oid and **gateway.auth.password** should have OCPP password
5.2. The property **gateway.url.ocp** should have /objects/**[EVCharger-1 oid]**/properties/ocpIpPort
5.3. Got to `vicinity-vas-dreven/end-user-api---service/` and run `mvn compile com.google.cloud.tools:jib-maven-plugin:1.6.1:dockerBuild`
6. Edit `vicinity-vas-dreven/middleware/src/main/resources/application.properties`
6.1. The properties **gateway.auth.user** should have the OCPP oid and **gateway.auth.password** should have OCPP password
6.2. Got to `vicinity-vas-dreven/middleware/` and run `mvn compile com.google.cloud.tools:jib-maven-plugin:1.6.1:dockerBuild`
7. Edit **REVERCE_GEOCODING_API_KEY** in ` mobility-service-provider---service/msp/resources/infrastructure.py`. This should be a google api key.<br>
8. In `vicinity-vas-dreven/` execute: `docker-compose up -d`
All necessary components should now be running.
## Setup Provider
1. Create instance of provider by sending a POST to the MSP Service
```
curl -X POST \
  http://{HOST}:19998/providers \
  -H 'Content-Type: application/json' \
  -d '{"name": "{PROVIDER_NAME}" }'
```
2. Create wallet for provider. Id comes from the step one's response.
```
curl -X POST \
  http://{HOST}:19998/providers/{PROVIDER_ID}/wallet \
  -H 'Content-Type: application/json' \
  -d '{"entropy": "entropy_salt"}'
```
3. Transfer funds to Created wallet. Wallet address comes on the response from step 2. For the sake of exampling, use Metamask.
4. Create Pricing contract.
```
curl -X POST \
  http://{HOST}:19998/providers/{PROVIDER_ID}/pricingcontract \
  -H 'Content-Type: application/json' \
  -d '{"initial_price": {PRICE_PER_WATT_IN_WEI}}'
```
All setup for a specific provider should be done.
## Setup charger infrastructure
1. Associate charger with Provider
```
curl -X POST \
  http://{HOST}:19998/providers/{PROVIDER_ID}/infrastructures \
  -H 'Content-Type: application/json' \
  -d '{
  "vicinity_oid": "{INFRA_ID_FROM_VICINITY_CONFIGURATION}",
  "longitude": {CHARGER_LONGITUDE},
  "latitude": {CHARGER_LATITUDE},
  "name": "{CHARGER_NAME}"
}'
#  {"vicinity_oid": "EVCharger-1", "longitude": -7.741017, "latitude": 37.443155, "name": "Enercoutim - Charger 001"}
```
## Setup client account
1. Scan QR code from the card that we'll be use to charge. If no QR printed in the card, convert the idTag to QR code.
2. In the mobile app, create a new account following the normal procedure. (**FIX THINGS DESCRIPTION OCP IP PORT TO POINT TO THE CONTAINER NAME INSTEAD OF STATIC IP**)
3. Add funds to client wallet (Ether) for transactions fee porposes
4. Add funds (DAI) to, later, transfer to the provider contract
## Sign contract with provider
1. In the mobile app, go to *wallet tab* -> *add provider*, and click '*ADD*' for the intended provider
2. Transfer funds (DAI) to contract
## Charging sequence
1. Make sure signature is true
2. Plug the charging cable into the car
2. Scan the RFID Card on the charger
3. When finished charging, scan the RFID card again
4. Unplug the charge from the car
3. Drive green! :D
## How to test
To access STEVE/OCP User interface, in a browser visit the url **host**:8182/steve/manager/signin. The user is **admin** and the pass is **1234**
To test MSP, in a browser visit the url **host**:19998/swagger
To test MOBILE-API, in a browser visit the url **host**:8080/swagger-ui.html
