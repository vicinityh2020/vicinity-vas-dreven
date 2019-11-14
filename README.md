# vicinity-vas-dreven

## Requirements
Install docker, docker-compose and maven

## How to run
1. Create a vicinity access point in neighbourhood manager.
2. Edit `vicinity-vas-dreven/ev-charger---device-/config/agent/config-1.json`. Change the `agent-id` and `password` in the `credentials` to reflect the ones created in step 1.
3. In `vicinity-vas-dreven/` execute: `docker-compose up -d postgres adapter agent gateway`
4. Go to neighbourhood manager and enable the EVCharger-1 and OCPP
5. Edit `vicinity-vas-dreven/end-user-api---service/src/main/resources/application.properties`
5.1. The properties **gateway.auth.user** should have the OCPP oid and **gateway.auth.password** should have OCPP password
5.2. The property **gateway.url.ocp** should have /objects/**[EVCharger-1 oid]**/properties/ocpIpPort
6. Edit `vicinity-vas-dreven/middleware/src/main/resources/application.properties`
6.1. The properties **gateway.auth.user** should have the OCPP oid and **gateway.auth.password** should have OCPP password
7. Edit **REVERCE_GEOCODING_API_KEY** in ` mobility-service-provider---service/msp/resources/infrastructure.py`. This should be a google api key.
8. In `vicinity-vas-dreven/` execute: `docker-compose up -d`

All necessary components should now be running

## How to test
To access STEVE/OCP User interface, in a browser visit the url **host**:8182/steve/manager/signin. The user is **admin** and the pass is **1234**
To test MSP, in a browser visit the url **host**:19998/swagger
To test MOBILE-API, in a browser visit the url **host**:8080/swagger-ui.html
