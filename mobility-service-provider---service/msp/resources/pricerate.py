import falcon
import json
from falcon import HTTPBadRequest, HTTPNotFound, HTTPForbidden, HTTP_200, HTTP_201, HTTP_204
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel, walletModel, pricingContractModel
from msp.resources import BaseResource
from ethereum.web3_connection import web3
from msp.schemas.pricerate import price_rate_patch

PATH_TO_JSON = 'config/eth/pricing.json'
PRICING_CONTRACT_ABI = 'pricing_abi'
HEX_0x00 = '0x0000000000000000000000000000000000000000'
ADJUST_PRICING_FUNCTION_GAS_CONSUMPTION = 39014
GAS_TO_ADD = 1000000

class PriceRateResource(BaseResource):
    """
    API Resource to set and get prices for each provider. This resource exposes
    an Option, GET, PATCH methods. This converts contracts data
     into/from DB models. All methods translate keystone URI to internal URI.
    """

    def on_get(self, req, resp, **kwargs):
        """Get rate of provider's id
        ---
        summary: Fetches a rate practiced by provider's ID
        description: Endpoint that retrieves rate
        parameters:
            - in: path
              name: id
              description: id of provider
              schema:
                type: integer
        tags:
        - price_rate
        responses:
            200:
                description: OK
            404:
                description: Not found
        """

        PROVIDER_ID = kwargs.get('id')
        CONTRACT_ADDRESS = 'address'

        provider = providerModel.ProviderModel.get_by_id(
                self.db.session, PROVIDER_ID)

        if not provider:
            raise HTTPNotFound(description="Entry not found", code = 5)

        pricingContract_list = pricingContractModel.PricingContractModel.get_generic(
            self.db.session, provider_id=provider.id)

        if not pricingContract_list:
            raise HTTPNotFound(description="Entry not found", code = 13)

        pricingContract = [model.as_dict for model in pricingContract_list]

        if not pricingContract:
            raise HTTPNotFound(description="Entry not found", code = 13)

        contractAddress = pricingContract[len(pricingContract)-1].get(CONTRACT_ADDRESS)

        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)

        abi = data.get(PRICING_CONTRACT_ABI)
        contract = web3.eth.contract(address=contractAddress, abi=abi)

        rate = contract.functions.finalPrice().call()

        resp.status = HTTP_200
        resp.media = {
            "provider_id": provider.id,
            "pricing_contract": contractAddress,
            "price_rate": rate
        }



    @validate(price_rate_patch)
    def on_patch(self, req, resp, **kwargs):
        """Patch price rate
        ---
        summary: Updates the price practiced by provider' id
        description: Endpoint that updates price
        tags:
        - price_rate
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              description: id of provider
        requestBody:
            description: Object that contains key *price_rate*
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            price_rate:
                                type: integer
                        required:
                        - price_rate
        responses:
            200:
                description: OK
            400:
                description: Bad request
            404:
                description: Not found
        """

        PROVIDER_ID = kwargs.get('id')
        CONTRACT_ADDRESS = 'address'
        PRICE_RATE_TO_SET = req.media.get('price_rate')

        provider = providerModel.ProviderModel.get_by_id(
                self.db.session, PROVIDER_ID)

        if not provider:
            raise HTTPNotFound(description="Entry not found", code = 5)

        wallet = walletModel.WalletModel.get_by_id(
            self.db.session, provider.wallet_id)

        if wallet.address is None or wallet.privKey is None:
            raise  HTTPNotFound(description="Entry not found", code = 10)

        pricingContract_list = pricingContractModel.PricingContractModel.get_generic(
            self.db.session, provider_id=provider.id)

        if not pricingContract_list:
            raise HTTPNotFound(description="Entry not found", code = 13)

        pricingContract = [model.as_dict for model in pricingContract_list]

        if not pricingContract:
            raise HTTPNotFound(description="Entry not found", code = 13)

        contractAddress = pricingContract[len(pricingContract)-1].get(CONTRACT_ADDRESS)

        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)

        abi = data.get(PRICING_CONTRACT_ABI)
        contract = web3.eth.contract(address=contractAddress, abi=abi)

        txn = contract.functions.adjustPricing(PRICE_RATE_TO_SET).buildTransaction({
            'nonce': web3.eth.getTransactionCount(wallet.address),
            'gas': ADJUST_PRICING_FUNCTION_GAS_CONSUMPTION + GAS_TO_ADD
            # GAS SHOULD USE ESTIMATEGAR() BUT
            # ValueError: {'code': -32016, 'message': 'The execution failed due to an exception.'}
            # There is a miscompatibility with geth (Infuras client)
            })

        txn_signed = web3.eth.account.signTransaction(txn, wallet.privKey)

        try:
            txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
        except ValueError :
            raise HTTPForbidden(description="Insuficient balance", code=12)

        web3.eth.waitForTransactionReceipt(txn_hash)

        resp.status = HTTP_200
        resp.media = {
            "new_price": PRICE_RATE_TO_SET,
            "tx_hash": txn_hash.hex()
        }