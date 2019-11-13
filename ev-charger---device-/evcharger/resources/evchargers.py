import falcon
import json
import os
from datetime import datetime
from falcon import HTTPBadRequest, HTTPNotFound, HTTP_200, HTTP_201, HTTP_204, HTTP_404
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from evcharger.utils.toTimestamp import to_timestamp
from evcharger.resources import BaseResource
from evcharger.schemas.evcharger import evcharger_update
from evcharger.db.models import infrastructureModel
from evcharger.db.models import providerModel
from evcharger.db.models import walletModel

PATH_TO_THING_DESCRIPTION = './objects'
THING_DESCRIPTION_NAME = 'thing_description.json'
#os.chdir(PATH_TO_THING_DESCRIPTION) NAO FAZER!!

class EVchargersResource(BaseResource):
    """
    EVCharger API to interact with different evchargers within the BD model.
    Endpoints:
        [GET | PUT] - /objects/{oid}/properties/{pid}
        [GET] - /objects
    """

    def on_get(self, req, resp, **kwargs):
        """
        [GET] - /objects/{oid}/properties/{pid}
        Endpoint that retrieves to Vicinity agent the value of Property ID (PID)
        from Object ID (OID)
        :return:
            200 OK - Value of {pid} is returned sucessfully
            404 NOT FOUND - {oid} was not found on db
        """
        print(kwargs.get('oid'))
        model4evcharger = infrastructureModel.InfrastructureModel.get_generic(
            self.db.session, vicinity_oid=kwargs.get('oid'))

        if model4evcharger is not None:
                resp.status = HTTP_200
                resp.media = {
                    'vicinity_oid': kwargs.get('oid'),
                    kwargs.get('pid'): model4evcharger[len(model4evcharger)-1].as_dict.get(kwargs.get('pid'))
                }
        else:
            raise HTTPNotFound(description="Entry not found", code = 4)

    @validate(evcharger_update)
    def on_put(self, req, resp, **kwargs):
        """
        [PUT] - /objects/{oid}/properties/{pid}
        Endpoint that changes value of Property ID (PID) of Object ID (OID)
        :return:
            200 OK - {pid} value of {oid} is successfully updates
            404 NOT FOUND - {oid} was not found on db
        """

        PID = kwargs.get('pid')
        OID = kwargs.get('oid')

        model4evcharger = infrastructureModel.InfrastructureModel.get_generic(
            self.db.session, vicinity_oid=OID)

        if model4evcharger is not None:
            model4evcharger = model4evcharger[len(model4evcharger)-1]

            try:
                model4evcharger.update(self.db.session, **req.media)
            except IntegrityError:
                raise HTTPBadRequest(description="Unique constraint failed", code=3)


            resp.status = HTTP_200
            resp.media = {
                'vicinity_oid': model4evcharger.vicinity_oid,
                PID: model4evcharger.as_dict.get(PID),
                'updated_on': model4evcharger.updated_on
            }
        else:
            raise HTTPNotFound(description="Entry not found", code = 4)

    def on_get_TD(self, req, resp):
        """
        [GET] - /objects
        Endpoint that answers to Vicinity agent and retrieves thing description
        to Active discovery
        :return:
            200 OK - returns thing description
        """


        with open(os.path.join(PATH_TO_THING_DESCRIPTION, THING_DESCRIPTION_NAME)) as json_file:
            data = json.load(json_file)

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(data)

    def on_post(self, req, resp):
        """
        [POST] - /infra
        TEST PORPUSES ONLY! Inserts provider-wallet-infrastructure
        """

        model4wallet = walletModel.WalletModel(
            address=req.media.get('address')
        )



        try:
            model4wallet.save(self.db.session)
        except IntegrityError:
            raise HTTPBadRequest(description="Unique constraint failed", code=1)

        model4provider = providerModel.ProviderModel(
            name=req.media.get('name'),
            wallet_id=model4wallet.id
        )


        try:
            model4provider.save(self.db.session)
        except IntegrityError:
            r
            raise HTTPBadRequest(description="Unique constraint failed", code=2)

        model4infrastructure = infrastructureModel.InfrastructureModel(
            provider_id=model4provider.id,
            vicinity_oid=req.media.get('vicinity_oid')
        )


        try:
            model4infrastructure.save(self.db.session)
        except IntegrityError:
            #AQUI É PRECISO DAR DELETE DA WALLET CRIADA ANTES
            raise HTTPBadRequest(description="Unique constraint failed", code=2)


        resp.status = HTTP_201
        resp.media = {
            'provider_id': model4provider.id,
            'wallet_id': model4provider.wallet_id,
            'infrastructure_id': model4infrastructure.id,
            'created_on': model4provider.created_on
        }

