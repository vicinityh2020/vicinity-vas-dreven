import falcon
import json
from falcon import HTTPBadRequest, HTTPNotFound, HTTPForbidden, HTTP_200, HTTP_201, HTTP_204
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel, walletModel, pricingContractModel, endUserModel, multisigContractModel, infrastructureModel
from msp.resources import BaseResource
from ethereum.web3_connection import web3
from msp.schemas.transaction import transaction_start_post


PATH_TO_JSON = 'config/eth/multisig.json'
MULTISIG_CONTRACT_ABI = 'multisig_abi'
HEX_0x00 = '0x0000000000000000000000000000000000000000'
CHARGE_ENDUSER_FUNCTION_GAS_CONSUMPTION = 164867
GAS_TO_ADD = 1000000

class TransactionStartResource(BaseResource):
    """
    API Resource to set and post transctions for each charging session. This resource exposes
    POST methods. This converts contracts data into/from DB models. All methods translate
    keystone URI to internal URI.
    """

    @validate(transaction_start_post)
    def on_post(self, req, resp):
        """Post a start transaction
        ---
        summary: Creates the start of a transaction
        description: Endpoint that creates the beginning of a transaction
        tags:
        - transactions
        consumes:
        - application/json
        produces:
        - application/json
        requestBody:
            description: Object that contains key object to start transaction
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            idTag:
                                type: string
                            meterValue:
                                type: integer
                            vicinityOid:
                                type: string
                        required:
                        - idTag
                        - meterValue
                        - vicinityOid
        responses:
            201:
                description: Created
            400:
                description: Bad request
            404:
                description: Not Found
        """

        USER_IDTAG = req.media.get('idTag')
        METERVALUE_START = req.media.get('meterValue')
        VICINITY_OID = req.media.get('vicinityOid')
        print("Starting Tx for idTag {} with meter value {}".format(USER_IDTAG, METERVALUE_START))
        endUser_list = endUserModel.EndUserModel.get_generic(
            self.db.session, idTag=USER_IDTAG)

        if not endUser_list:
            raise HTTPNotFound(description="Entry not found", code = 16)

        endUser = [model.as_dict for model in endUser_list]
        endUser = endUser[len(endUser)-1]

        if not endUser:
            raise HTTPNotFound(description="Entry not found", code = 16)

        infrastructure_list = infrastructureModel.InfrastructureModel.get_generic(
            self.db.session, vicinity_oid=VICINITY_OID)

        if not infrastructure_list:
            raise HTTPNotFound(description="Entry not found", code = 8)

        infrastructure = [model.as_dict for model in infrastructure_list]
        infrastructure = infrastructure[len(infrastructure)-1]

        if not infrastructure:
            raise HTTPNotFound(description="Entry not found", code = 8)

        infrastructure = infrastructureModel.InfrastructureModel.get_by_id(
            self.db.session, infrastructure.get('id'))

        try:
            infrastructure.update(self.db.session, meterValue=METERVALUE_START, lastStartMeterValue=METERVALUE_START)
        except IntegrityError:
            raise HTTPBadRequest(description="Unique constraint failed", code=3)

        resp.status = HTTP_201
        resp.media = {
            'infrastructure_id': infrastructure.id,
            'meterValue': infrastructure.meterValue,
            'updated_on': infrastructure.updated_on
        }






