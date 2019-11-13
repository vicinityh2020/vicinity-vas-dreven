import falcon
import json
import requests
import aumbry

from falcon import HTTPBadRequest, HTTPNotFound, HTTP_200, HTTP_201, HTTP_204
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel
from msp.db.models import infrastructureModel
from msp.resources import BaseResource
from msp.schemas.infrastructure import  infrastructure_post

URL_BASE_OCPP =  "http://ocpp:8180" #ocpp
URL_ADD_CHARGER_POINT = "/steve/chargePoint"

URL_BASE_AGENT = 'http://agent:9997'    #agent
URL_GET_AGENT_CONFIG = '/agent/configuration'

REVERSE_GEOCODING_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"
REVERCE_GEOCODING_API_KEY = "AIzaSyA5PbOYkB4i9shatP_LKaa5uDy_oj1wCcM"

class InfrastructureCollection(BaseResource):
    def on_get(self, req, resp):
        """Get all infrastructures
        ---
        summary: Fetches every existent infrastructure
        description: Endpoint that retrieves every infrastructure
        tags:
        - infrastructures
        responses:
            200:
                description: OK
        """

        model_infrastructures_list = infrastructureModel.InfrastructureModel.get_all(self.db.session)

        infrastructures = [model.as_dict for model in model_infrastructures_list]

        resp.status = HTTP_200
        resp.media = {
            "infrastructures": infrastructures
        }


class InfrastructureResource(BaseResource):
    """
    API Resource to interact with Infrastructures BD model. This resource exposes
    an Option, GETand POST methods. This converts infrastructure data
    into/from DB models. All methods translate keystone URI to internal URI.
    """

    def on_get(self, req, resp, **kwargs):
        """Get an infrastructure by its  ID
        ---
        summary: Fetches an infrastructure by  ID
        description: Endpoint that retrieves infrastructure by  ID
        parameters:
            - in: path
              name: id
              description: id of infrastructure
              schema:
                type: integer
        tags:
        - infrastructures
        responses:
            200:
                description: OK
            404:
                description: Not found
        """

        INFRASTRUCTURE_ID = kwargs.get('id')

        infrastructure = infrastructureModel.InfrastructureModel.get_by_id(
            self.db.session, INFRASTRUCTURE_ID)

        if infrastructure:
            resp.status = HTTP_200
            resp.media = {
                "infrastructure": infrastructure.as_dict
            }
        else:
            raise HTTPNotFound(description="Entry not found", code = 8)

class InfrastructureResourceByProvider(BaseResource):
    def on_get(self, req, resp, **kwargs):
        """Get an infrastructure by its provider's ID
        ---
        summary: Fetches an infrastructure by its provider's ID
        description: Endpoint that retrieves infrastructure by its provider's ID
        parameters:
            - in: path
              name: id
              description: id of provider
              schema:
                type: integer
        tags:
        - infrastructures
        responses:
            200:
                description: OK
            404:
                description: Not found
        """

        PROVIDER_ID = kwargs.get('id')

        model_infrastructures_list = infrastructureModel.InfrastructureModel.get_generic(
            self.db.session, provider_id=PROVIDER_ID)

        if not model_infrastructures_list:
            raise HTTPNotFound(description="Entry not found", code = 8)

        infrastructures = [model.as_dict for model in model_infrastructures_list]

        resp.status = HTTP_200
        resp.media = {
            "infrastructure": infrastructures
        }


    @validate(infrastructure_post)
    def on_post(self, req, resp, **kwargs):
        """Post an infrastructure
        ---
        summary: Creates an infrastructure resource
        description: Endpoint that creates an infrastructure
        tags:
        - infrastructures
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
            - in: path
              name: id
              description: id of provider that creates infrastructure
              schema:
                type: integer
        requestBody:
            description: Object that contains keys to create infrastructure
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            vicinity_oid:
                                type: string
                            longitude:
                                type: number
                            latitude:
                                type: number
                            name:
                                type: string
                        required:
                        - vicinity_oid
                        - longitude
                        - latitude
                        - name
        responses:
            201:
                description: Created
            400:
                description: Bad request
            404:
                description: Not Found
        """

        VICINITY_OID = req.media.get('vicinity_oid')
        LONGITUDE = req.media.get('longitude')
        LATITUDE = req.media.get('latitude')
        NAME = req.media.get('name')
        PROVIDER_ID = kwargs.get('id')
        ADAPTERS = 'adapters'
        THINGS = 'things-by-oid'
        INFRA_ID = 'infra-id'
        OID = 'oid'
        address_name = None

        params = (
            ('latlng', str(LATITUDE) + ',' + str(LONGITUDE)),
            ('key', REVERCE_GEOCODING_API_KEY),
        )
        res_array = requests.get(REVERSE_GEOCODING_ENDPOINT, params=params).json().get('results')

        if not res_array:
            raise HTTPBadRequest(description="Invalid coordinates", code = 23)

        for component in res_array:
            if 'street_address' in component.get('types'):
                address_name = component.get('formatted_address')
                break
        if address_name == None:
            for component in res_array:
                if 'route' in component.get('types'):
                    address_name = component.get('formatted_address')
                    break
        if address_name == None:
            raise HTTPBadRequest(description="Unknown address", code = 24)


        agent_conf = requests.get(URL_BASE_AGENT + URL_GET_AGENT_CONFIG)
        array_of_things = agent_conf.json().get(THINGS)
        chargeBoxId = None

        for t in array_of_things:
            if (t.get(INFRA_ID) == VICINITY_OID):
                chargeBoxId = t.get(OID)
                break

        if not chargeBoxId:
            raise HTTPNotFound(description="Entry not found", code = 20)


        add_charge_box = requests.post(URL_BASE_OCPP + URL_ADD_CHARGER_POINT,
        data=json.dumps({'chargeBoxId':chargeBoxId,'description': VICINITY_OID}).encode('utf8'),
        headers={"content-type": "application/json", "accept": "application/json"})

        if (add_charge_box.status_code != 200 ):
            raise HTTPBadRequest(description="OCPP Error", code=21)

        infrastructure = infrastructureModel.InfrastructureModel(
            vicinity_oid=VICINITY_OID, provider_id=PROVIDER_ID, longitude=LONGITUDE, latitude=LATITUDE, name=NAME, address=address_name)

        provider = providerModel.ProviderModel.get_by_id(
            self.db.session, PROVIDER_ID)

        if not provider:
            raise HTTPNotFound(description="Entry not found", code = 5)

        try:
            infrastructure.save(self.db.session)
        except IntegrityError:
            raise HTTPBadRequest(description="Unique constraint failed", code=15)

        resp.status = HTTP_201
        resp.media = {
            'infrastructure_id': infrastructure.id,
            'created_on': infrastructure.created_on
        }
