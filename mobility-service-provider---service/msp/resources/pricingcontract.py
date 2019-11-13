import falcon
import json
from falcon import HTTPBadRequest, HTTPNotFound, HTTPForbidden, HTTP_200, HTTP_201, HTTP_204
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel, walletModel, pricingContractModel
from msp.resources import BaseResource
from ethereum.web3_connection import web3
from msp.schemas.pricingcontract import pricing_contract_post
#from msp.utils.factory_address import pricing_factory_address, pricing_factory_abi

PATH_TO_JSON = 'config/eth/factory_address.json'
PRICING_CONTRACT_ADDRESS = 'pricing_factory_address'
PRICING_CONTRACT_ABI = 'pricing_factory_abi'
HEX_0x00 = '0x0000000000000000000000000000000000000000'
GAS_TO_ADD = 1000000

class PricingcontractCollection(BaseResource):
    def on_get(self, req, resp):
        """Get all pricing contracts
        ---
        summary: Fetches every existent pricing contract
        description: Endpoint that retrieves every pricing contract
        tags:
        - pricing_contracts
        responses:
            200:
                description: OK
        """

        pricingContract_list = pricingContractModel.PricingContractModel.get_all(
            self.db.session)

        if not pricingContract_list:
            raise HTTPNotFound(description="Entry not found", code = 13)

        pricingContract = [model.as_dict for model in pricingContract_list]

        if pricingContract:
            resp.status = HTTP_200
            resp.media = {
                "pricingContracts": pricingContract
            }
        else:
            raise HTTPNotFound(description="Entry not found", code = 13)

class PricingcontractResource(BaseResource):
    """
    API Resource to interact with Pricing Contracts BD model. This resource exposes
    an Option, GET, POST and PATCH methods. This converts contracts data
     into/from DB models. All methods translate keystone URI to internal URI.
    """
    def on_get(self, req, resp, **kwargs):
        """Get a pricing contract by  ID
        ---
        summary: Fetches pricing contract by its ID
        description: Endpoint that retrieves pricing contract by ID
        parameters:
            - in: path
              name: id
              description: id of pricing contract
              schema:
                type: integer
        tags:
        - pricing_contracts
        responses:
            200:
                description: OK
            404:
                description: Not found
        """
        PROVIDER_ID = kwargs.get('id')

        provider = providerModel.ProviderModel.get_by_id(
                self.db.session, PROVIDER_ID)

        if not provider:
            raise HTTPNotFound(description="Entry not found", code = 5)

        pricingContract_list = pricingContractModel.PricingContractModel.get_generic(
            self.db.session, provider_id=PROVIDER_ID)

        if not pricingContract_list:
            raise HTTPNotFound(description="Entry not found", code = 13)

        pricingContract = [model.as_dict for model in pricingContract_list]

        if pricingContract:
            resp.status = HTTP_200
            resp.media = {
                "pricingContract": pricingContract
            }
        else:
            raise HTTPNotFound(description="Entry not found", code = 13)



    @validate(pricing_contract_post)
    def on_post(self, req, resp, **kwargs):
        """Post a pricing contract
        ---
        summary: Creates a pricing contract to a provider's id
        description: Endpoint that creates pricing contract
        tags:
        - pricing_contracts
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              description: id of provider to create pricing contract
        requestBody:
            description: Object that contains key *initial_price*
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            initial_price:
                                type: integer
                        required:
                        - initial_price
        responses:
            200:
                description: OK
            400:
                description: Bad request
            404:
                description: Not found
        """

        INITIAL_PRICE_TO_SET = req.media.get('initial_price')
        PROVIDER_ID = kwargs.get('id')

        # Check if  provider exits
        provider = providerModel.ProviderModel.get_by_id(
                self.db.session, PROVIDER_ID)

        if not provider:
            raise  HTTPNotFound(description="Entry not found", code = 5)
        if not provider.wallet_id:
            raise HTTPNotFound(description="Entry not found", code = 6)

        # Check if provider has valid wallet
        wallet = walletModel.WalletModel.get_by_id(
            self.db.session, provider.wallet_id)

        if wallet.address is None or wallet.privKey is None:
            raise  HTTPNotFound(description="Entry not found", code = 10)

        # Check if provider does not have a pricing contract
        pricingContract_list = pricingContractModel.PricingContractModel.get_generic(
            self.db.session, provider_id=PROVIDER_ID)

        if pricingContract_list:
            raise HTTPBadRequest(description="Provider has contract", code=11)


        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)

        address = web3.toChecksumAddress(data[PRICING_CONTRACT_ADDRESS])
        abi = data[PRICING_CONTRACT_ABI]
        contract = web3.eth.contract(address=address, abi=abi)

        if contract.functions.getDeployedPricingByProvider(wallet.address).call() != HEX_0x00:
            raise HTTPBadRequest(description="Provider has contract", code=11)

        gas = contract.functions.createPricing(INITIAL_PRICE_TO_SET).estimateGas()
        txn = contract.functions.createPricing(INITIAL_PRICE_TO_SET).buildTransaction({
            'nonce': web3.eth.getTransactionCount(wallet.address),
            'gas': gas + GAS_TO_ADD
            })

        txn_signed = web3.eth.account.signTransaction(txn, wallet.privKey)

        try:
            txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
        except ValueError :
            raise HTTPForbidden(description="Insuficient balance", code=12)

        web3.eth.waitForTransactionReceipt(txn_hash)

        pricingContract = pricingContractModel.PricingContractModel(
            provider_id=provider.id,
            address=contract.functions.getDeployedPricingByProvider(wallet.address).call()
        )

        try:
            pricingContract.save(self.db.session)
        except IntegrityError:
            raise HTTPBadRequest(description="Unique constraint failed", code=14)


        resp.status = HTTP_201
        resp.media = {
            'provider': provider.id,
            'tx_hash': txn_hash.hex(),
            'address': contract.functions.getDeployedPricingByProvider(wallet.address).call(),
            'initial_price': INITIAL_PRICE_TO_SET,
        }

