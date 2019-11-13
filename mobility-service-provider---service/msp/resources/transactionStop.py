import falcon
import json
from falcon import HTTPBadRequest, HTTPNotFound, HTTPForbidden, HTTP_200, HTTP_201, HTTP_204
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel, walletModel, pricingContractModel, endUserModel, multisigContractModel, infrastructureModel
from msp.resources import BaseResource
from ethereum.web3_connection import web3
from msp.schemas.transaction import transaction_stop_post


PATH_TO_JSON = 'config/eth/multisig.json'
MULTISIG_CONTRACT_ABI = 'multisig_abi'
HEX_0x00 = '0x0000000000000000000000000000000000000000'
CHARGE_ENDUSER_FUNCTION_GAS_CONSUMPTION = 164867
GAS_TO_ADD = 1000000

class TransactionStopResource(BaseResource):
    @validate(transaction_stop_post)
    def on_post(self, req, resp):
        """Post a stop transaction
        ---
        summary: Creates the stop of a transaction
        description: Endpoint that creates the finish of a transaction
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
        METERVALUE_STOP = req.media.get('meterValue')
        VICINITY_OID = req.media.get('vicinityOid')
        CONTRACT_ADDRESS = 'address'

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

        provider = providerModel.ProviderModel.get_by_id(
            self.db.session, infrastructure.provider_id)

        if not provider:
            raise HTTPNotFound(description="Entry not found", code=5)

        wallet = walletModel.WalletModel.get_by_id(
            self.db.session, provider.wallet_id)

        if not wallet:
            raise HTTPNotFound(description="Entry not found", code=6)

        multisig_list = multisigContractModel.MultisigContractModel.get_generic(
            self.db.session, enduser_id=endUser.get('id'))

        if not multisig_list:
            raise HTTPNotFound(description="Entry not found", code = 18)

        multisig = [model.as_dict for model in multisig_list]
        multisig = multisig[len(multisig)-1]

        if not multisig:
            raise HTTPNotFound(description="Entry not found", code = 18)

        contractAddress = multisig.get(CONTRACT_ADDRESS)

        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)

        abi = data.get(MULTISIG_CONTRACT_ABI)
        contract = web3.eth.contract(address=contractAddress, abi=abi)

        # CHECKER AQUI

        #if (round((CURRENT_METERVAMETERVALUE_STOPLUE - infrastructure.lastStartMeterValue) * rate) < costumer_balance):

        txn = contract.functions.chargeEndUser(abs(METERVALUE_STOP - infrastructure.lastStartMeterValue)).buildTransaction({
            'nonce': web3.eth.getTransactionCount(wallet.address),
            'gas':  CHARGE_ENDUSER_FUNCTION_GAS_CONSUMPTION + GAS_TO_ADD
            # GAS SHOULD USE ESTIMATEGAS() BUT
            # ValueError: {'code': -32016, 'message': 'The execution failed due to an exception.'}
            # There is a miscompatibility with geth (Infuras client)
            })

        txn_signed = web3.eth.account.signTransaction(txn, wallet.privKey)

        try:
            txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
        except ValueError :
            raise HTTPForbidden(description="Insuficient balance", code=12)

        web3.eth.waitForTransactionReceipt(txn_hash)

        if web3.eth.getTransactionReceipt(txn_hash).status is 0:
            raise HTTPForbidden(description="Transaction hash: {}".format(txn_hash.hex()), code=19)

        try:
            infrastructure.update(self.db.session, meterValue=METERVALUE_STOP)
        except IntegrityError:
            raise HTTPBadRequest(description="Unique constraint failed", code=3)


        resp.status = HTTP_200
        resp.media = {
            "tx_hash": txn_hash.hex(),

        }
