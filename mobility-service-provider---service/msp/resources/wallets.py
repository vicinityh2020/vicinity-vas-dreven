import falcon
import json

from falcon import HTTPBadRequest, HTTPNotFound, HTTP_200, HTTP_201, HTTP_204, HTTP_404
from falcon.media.validators.jsonschema import validate
from sqlalchemy.exc import IntegrityError
from msp.db.models import providerModel
from msp.db.models import walletModel
from msp.resources import BaseResource
from msp.schemas.wallet import wallet_post, wallet_patch

from ethereum.web3_connection import web3
from eth_account import Account

PRIVKEY = 'privKey'

class WalletCollection(BaseResource):
    def on_get(self, req, resp):
        """Get all wallets
        ---
        summary: Fetches every existent wallet
        description: Endpoint that retrieves every wallet
        tags:
        - wallets
        responses:
            200:
                description: OK
        """


        model_wallets_list = walletModel.WalletModel.get_all(self.db.session)

        wallets = [model.as_dict for model in model_wallets_list]
        remove_privateKeys = [i.pop(PRIVKEY) for i in wallets]

        resp.status = HTTP_200
        resp.media = {
            "wallets": wallets
        }

class WalletsResource(BaseResource):
    """
    API Resource to interact with Wallets BD model. This resource exposes
    an Option, GET, POST and PATCH methods. This converts wallets data
     into/from DB models. All methods translate keystone URI to internal URI.
    """


    def on_get(self, req, resp, **kwargs):
        """Get a wallet by its provider id
        ---
        summary: Fetches a wallet by its provider id
        description: Endpoint that gets a wallet by its provider id
        tags:
        - wallets
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
            - in: path
              name: id
              description: id of provider
              schema:
                type: integer
        responses:
            200:
                description: OK
            404:
                description: Not Found
                code: 2
        """

        PROVIDER_ID = kwargs.get('id')
        provider = providerModel.ProviderModel.get_by_id(self.db.session, PROVIDER_ID)

        if provider:
            provider_wallet = walletModel.WalletModel.get_by_id(
                self.db.session, provider.wallet_id)

            provider_wallet = provider_wallet.as_dict

            remove_privateKey = provider_wallet.pop(PRIVKEY)

            resp.status = HTTP_200
            resp.media = {
                "wallet": provider_wallet
            }
        else:
            raise HTTPNotFound(description="Entry not found", code = 5)

    @validate(wallet_post)
    def on_post(self, req, resp, **kwargs):
        """Post a wallet
        ---
        summary: Creates a wallet for a certain provider
        description: Endpoint that creates a wallet for a specified provider id
        tags:
        - wallets
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
            - in: path
              name: id
              description: id of provider
              schema:
                type: integer
        requestBody:
            description: Object that contains key *entropy*
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            entropy:
                                type: string
                        required:
                        - entropy
        responses:
            201:
                description: Created
            400:
                description: Bad request
                code: 2
            404:
                description: Not Found
                code: 5
        """
        PROVIDER_ID = kwargs.get('id')
        PASSWORD = req.media.get('entropy')

        provider = providerModel.ProviderModel.get_by_id(
                self.db.session, PROVIDER_ID)

        if provider:

            acc = Account.create(PASSWORD)

            wallet = walletModel.WalletModel(
                 address=acc.address,
                 privKey=acc.privateKey.hex()
                 )

            try:
                wallet.save(self.db.session)
            except IntegrityError:
                raise HTTPBadRequest(description="Unique constraint failed", code=1)

            try:
                provider.update(self.db.session, wallet_id=wallet.id )
            except IntegrityError:
                raise HTTPBadRequest(description="Unique constraint failed", code=3)

            resp.status = HTTP_201
            resp.media = {
                'id': wallet.id,
                'address': wallet.address,
                'created_on': wallet.created_on
            }

        else:
            raise HTTPNotFound(description="Entry not found", code = 5)

'''
    @validate(wallet_patch)
    def on_patch(self, req, resp, **kwargs):
        """Patch a wallet
        ---
        summary: Updates a wallet resource  provider ID
        description: Endpoint that updates a wallet by provider id
        tags:
        - wallets
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              description: id of provider's wallet to patch
        requestBody:
            description: Object that contains key *entropy*, it provides randomness to the generation of the wallet keys
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            entropy:
                                type: string
                        required:
                        - entropy
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

        PROVIDER_ID = kwargs.get('id')
        PASSWORD = req.media.get('entropy')

        provider = providerModel.ProviderModel.get_by_id(
                self.db.session, PROVIDER_ID)

        if provider:
            provider_wallet = walletModel.WalletModel.get_by_id(
                self.db.session, provider.wallet_id)

            if provider_wallet:

                acc = Account.create(PASSWORD)

                try:
                    provider_wallet.update(self.db.session, address=acc.address, privKey=acc.privateKey.hex())
                except IntegrityError:
                    raise HTTPBadRequest(description="Unique constraint failed", code=3)

                resp.status = HTTP_201
                resp.media = {
                    'id': provider_wallet.id,
                    'address': provider_wallet.address,
                    'private_key': acc.privateKey.hex(),
                    'updated_on': provider_wallet.updated_on
                }

            else:
                raise HTTPNotFound(description="Entry not found", code = 6)
        else:
            raise HTTPNotFound(description="Entry not found", code = 5)
'''

