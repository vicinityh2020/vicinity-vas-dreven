import falcon
import json



from falcon import HTTPBadRequest, HTTPNotFound, HTTP_200, HTTP_201, HTTP_204
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel
from msp.db.models import walletModel
from msp.resources import BaseResource
from msp.schemas.provider import p_update, p_post



class ProvidersCollection(BaseResource):
    def on_get(self, req, resp, **kwargs):
        """Get all providers
        ---
        summary: Fetches every existent provider
        description: Endpoint that retrieves every providers
        tags:
        - providers
        responses:
            200:
                description: OK
        """
        model_list = providerModel.ProviderModel.get_all(self.db.session)

        providers = [model.as_dict for model in model_list]

        resp.status = HTTP_200
        resp.media = {
            "providers": providers
        }

    @validate(p_post)
    def on_post(self, req, resp):
        """Post a provider
        ---
        summary: Creates a provider resource
        description: Endpoint that creates a provider
        tags:
        - providers
        consumes:
        - application/json
        produces:
        - application/json
        requestBody:
            description: Object that contains key *name*
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            name:
                                type: string
                        required:
                        - name
        responses:
            201:
                description: Created
            400:
                description: Bad request
                code: 2
        """
        PROVIDER_NAME = req.media.get('name')
        model4provider = providerModel.ProviderModel(
            name=PROVIDER_NAME)

        try:
            model4provider.save(self.db.session)
        except IntegrityError:
            raise HTTPBadRequest(description="Unique constraint failed", code=2)

        resp.status = HTTP_201
        resp.media = {
            'id': model4provider.id,
            'wallet_id': model4provider.wallet_id,
            'created_on': model4provider.created_on
        }


class ProvidersResource(BaseResource):
    """
    API Resource to interact with Providers BD model. This resource exposes
    an Option, GET, POST and PATCH methods. This converts providers data
     into/from DB models. All methods translate keystone URI to internal URI.
    """

    def on_get(self, req, resp, **kwargs):
        """Get a provider by its ID
        ---
        summary: Fetches a provider by its ID
        description: Endpoint that retrieves provider by ID
        parameters:
            - in: path
              name: id
              description: id of provider to get
              schema:
                type: integer
        tags:
        - providers
        responses:
            200:
                description: OK
            404:
                description: Not found
                code: 5
        """
        PROVIDER_ID = kwargs.get('id')


        provider = providerModel.ProviderModel.get_by_id(
            self.db.session, PROVIDER_ID)

        if not provider:
            raise HTTPNotFound(description="Entry not found", code = 5)

        resp.status = HTTP_200
        resp.media = {
            "provider": provider.as_dict
        }

    @validate(p_update)
    def on_patch(self, req, resp, **kwargs):
        """Patch a provider
        ---
        summary: Updates a provider resource by ID
        description: Endpoint that updates a provider by id
        tags:
        - providers
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              description: id of provider to patch
        requestBody:
            description: Object that contains key *name*
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            name:
                                type: string
                        required:
                        - name
        responses:
            200:
                description: OK
            400:
                description: Bad request
                code: 3
            404:
                description: Not found
                code: 5
        """

        if 'id' in kwargs:
            provider = providerModel.ProviderModel.get_by_id(
                self.db.session, kwargs.get('id'))

            if provider:
                try:
                    provider.update(self.db.session, **req.media)
                except IntegrityError:
                    raise HTTPBadRequest(description="Unique constraint failed", code=3)

                resp.status = HTTP_200
                resp.media = {
                    'id': provider.id,
                    'name': provider.name,
                    'updated_on': provider.updated_on
                }
            else:
                raise HTTPNotFound(description="Entry not found", code = 5)
        else:
            raise HTTPBadRequest(description="URI format failed", code=7)


