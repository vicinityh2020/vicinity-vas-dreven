import falcon
import json
import requests
from falcon import HTTPBadRequest, HTTPNotFound, HTTPForbidden, HTTP_200, HTTP_201, HTTP_204
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel, walletModel, infrastructureModel, pricingContractModel, endUserModel, multisigContractModel
from msp.resources import BaseResource
from ethereum.web3_connection import web3
from msp.schemas.metervalue import metervalue_put

URL_BASE_OCPP =  "http://ocpp:8180"
URL_STOP_REMOTE_TRANSACTION = "/steve/transaction"


PATH_TO_MULTISIG_JSON = 'config/eth/multisig.json'
MULTISIG_CONTRACT_ABI = 'multisig_abi'
PATH_TO_PRICING_JSON = 'config/eth/pricing.json'
PRICING_CONTRACT_ABI = 'pricing_abi'
HEX_0x00 = '0x0000000000000000000000000000000000000000'
CHARGE_ENDUSER_FUNCTION_GAS_CONSUMPTION = 164867
GAS_TO_ADD = 1000000

class MetervalueResource(BaseResource):
    """
    API Resource to post each metervalue state transition. This resource exposes
    an Option Post method. This converts contracts data into/from DB models.
    All methods translate keystone URI to internal URI.
    """

    @validate(metervalue_put)
    def on_put(self, req, resp):
        """Put a meter value
        ---
        summary: Updates the metervalue of the tx
        description: Endpoint that updates the metervalue
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
        CURRENT_METERVALUE = req.media.get('meterValue')
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

        pricingContract_list = pricingContractModel.PricingContractModel.get_generic(
            self.db.session, provider_id=provider.id)

        if not pricingContract_list:
            raise HTTPNotFound(description="Entry not found", code = 13)

        pricingContract = [model.as_dict for model in pricingContract_list]

        if not pricingContract:
            raise HTTPNotFound(description="Entry not found", code = 13)

        contractAddress_pricing = pricingContract[len(pricingContract)-1].get(CONTRACT_ADDRESS)

        with open(PATH_TO_PRICING_JSON) as json_file:
            data = json.load(json_file)

        abi_pricing = data.get(PRICING_CONTRACT_ABI)
        contract_pricing = web3.eth.contract(address=contractAddress_pricing, abi=abi_pricing)

        rate = contract_pricing.functions.finalPrice().call()

        multisig_list = multisigContractModel.MultisigContractModel.get_generic(
            self.db.session, enduser_id=endUser.get('id'))

        if not multisig_list:
            raise HTTPNotFound(description="Entry not found", code = 18)

        multisig = [model.as_dict for model in multisig_list]
        multisig = multisig[len(multisig)-1]

        if not multisig:
            raise HTTPNotFound(description="Entry not found", code = 18)

        contractAddress_multisig = multisig.get(CONTRACT_ADDRESS)

        with open(PATH_TO_MULTISIG_JSON) as json_file:
            data = json.load(json_file)

        abi_multisig = data.get(MULTISIG_CONTRACT_ABI)
        contract_multisig = web3.eth.contract(address=contractAddress_multisig, abi=abi_multisig)

        costumer_balance = contract_multisig.functions.balanceOfContract().call()





        infrastructure.update(self.db.session, meterValue=CURRENT_METERVALUE)

        print(rate)
        print(round((CURRENT_METERVALUE - infrastructure.lastStartMeterValue)*rate))
        print(costumer_balance)



        if (round((CURRENT_METERVALUE - infrastructure.lastStartMeterValue)*rate) < costumer_balance):
            print("BALANCE IS ENOUGH")
            resp.status = HTTP_201
            resp.media = {
                'infrastructure_id': infrastructure.id,
                'meterValue': infrastructure.meterValue,
                'updated_on': infrastructure.updated_on
            }

        else:
            print("CHARGE CLIENT AT THIS POINT!")
            txn = contract_multisig.functions.zerateEndUser().buildTransaction({
                'nonce': web3.eth.getTransactionCount(wallet.address),
                'gas':  CHARGE_ENDUSER_FUNCTION_GAS_CONSUMPTION + GAS_TO_ADD
                # GAS SHOULD USE ESTIMATEGAS() BUT
                # ValueError: {'code': -32016, 'message': 'The execution failed due to an exception.'}
                # There is a miscompatibility with geth (Infuras client)
                })

            txn_signed = web3.eth.account.signTransaction(txn, wallet.privKey)

            try:
                txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
            except ValueError as e:
                print(e)
                raise HTTPForbidden(description="Insuficient balance", code=12)

            web3.eth.waitForTransactionReceipt(txn_hash)

            if web3.eth.getTransactionReceipt(txn_hash).status is 0:
                print("Transaction hash: {}".format(txn_hash.hex()))
                raise HTTPForbidden(description="Transaction hash: {}".format(txn_hash.hex()), code=19)

            resp.status = HTTP_200
            resp.media = {
                'infrastructure_id': infrastructure.id,
                'meterValue': infrastructure.meterValue,
                'tx_hash': txn_hash.hex(),
                'updated_on': infrastructure.updated_on
            }

            print("STOP REMOTE TRANSACTION")
            stop_remote_transaction = requests.patch(URL_BASE_OCPP + URL_STOP_REMOTE_TRANSACTION,
            data=json.dumps({'description': VICINITY_OID}).encode('utf8'),
            headers={"content-type": "application/json", "accept": "application/json"})

            if (stop_remote_transaction.status_code != 200 ):
                raise HTTPBadRequest(description="OCPP Error", code=21)




