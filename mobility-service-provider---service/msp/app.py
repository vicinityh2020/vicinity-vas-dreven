import falcon
import json
import pathlib
import yaml

from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin

from apispec import APISpec
from falcon_apispec import FalconPlugin
from falcon_swagger_ui import register_swaggerui_app

from msp.db import DBManager
from msp.middleware.context import ContextMiddleware
from msp.resources import providers, thing_description, wallets, infrastructure, pricingcontract, pricerate, discountrate, transactionStart, transactionStop, metervalue


SWAGGER_YAML_PATH = './msp/static/v1/swagger.json'
SWAGGERUI_URL = '/swagger'  # without trailing slash
PAGE_TITLE = 'Falcon Swagger Doc MSP'
FAVICON_URL = 'https://falconframework.org/favicon-32x32.png'
SCHEMA_URL = '/static/v1/swagger.json'
STATIC_PATH = pathlib.Path(__file__).parent / 'static'





class DefaultService(falcon.API):
    def __init__(self, cfg):
        super(DefaultService, self).__init__(
            middleware=[ContextMiddleware()]
        )

        self.cfg = cfg

        # Build an object to manage our db connections.
        mgr = DBManager(self.cfg.db.connection)
        mgr.setup()

        # Create resources and collections
        # thing_description_res = thing_description.ThingDescriptionResource()

        providers_res = providers.ProvidersResource(mgr)
        providers_col = providers.ProvidersCollection(mgr)

        wallets_res = wallets.WalletsResource(mgr)
        wallets_col = wallets.WalletCollection(mgr)

        infrastructure_res = infrastructure.InfrastructureResource(mgr)
        infrastructure_col = infrastructure.InfrastructureCollection(mgr)
        infrastructure_resByProvider = infrastructure.InfrastructureResourceByProvider(mgr)

        pricingcontract_res = pricingcontract.PricingcontractResource(mgr)
        pricingcontract_col = pricingcontract.PricingcontractCollection(mgr)

        pricerate_res = pricerate.PriceRateResource(mgr)

        discountrate_res = discountrate.DiscountRateResource(mgr)

        transactionStart_res = transactionStart.TransactionStartResource(mgr)
        transactionStop_res = transactionStop.TransactionStopResource(mgr)

        metervalue_res = metervalue.MetervalueResource(mgr)

        # Build routes
        # Thing description resource
        # self.add_route('/objects', thing_description_res)

        # Providers  resource
        self.add_route('/providers', providers_col)
        self.add_route('/providers/{id}', providers_res)

        # Wallets resource
        self.add_route('/providers/{id}/wallet', wallets_res)
        self.add_route('/wallets', wallets_col)

        # Infrastructure resource
        self.add_route('/infrastructures/{id}', infrastructure_res)
        self.add_route('/infrastructures', infrastructure_col)
        self.add_route('/providers/{id}/infrastructures', infrastructure_resByProvider)

        # Pricing contract resource
        self.add_route('/providers/{id}/pricingcontract', pricingcontract_res)
        self.add_route('/pricingcontracts', pricingcontract_col)

        # Pricing rate resource
        self.add_route('/providers/{id}/rate', pricerate_res)

        # Discount rate resource
        self.add_route('/providers/{id}/discount', discountrate_res)

        # Transactions resource
        self.add_route('/transaction/start', transactionStart_res)
        self.add_route('/transaction/stop', transactionStop_res)

        self.add_route('/metervalue', metervalue_res)

        # Swagger
        self.add_static_route('/static', str(STATIC_PATH))

        spec = APISpec(
            title="MSP API documentation",
            version="0.0.1",
            openapi_version='3.0.2',
            plugins=[FalconPlugin(self),
            MarshmallowPlugin(),
            ],
        )

        # Schemas
        # spec.components.schema('Provider', schema=Provider)

        # Resources
        spec.path(resource=providers_res)
        spec.path(resource=providers_col)
        spec.path(resource=wallets_res)
        spec.path(resource=wallets_col)
        spec.path(resource=infrastructure_res)
        spec.path(resource=infrastructure_col)
        spec.path(resource=infrastructure_resByProvider)
        spec.path(resource=pricingcontract_res)
        spec.path(resource=pricingcontract_col)
        spec.path(resource=pricerate_res)
        spec.path(resource=discountrate_res)
        spec.path(resource=transactionStart_res)
        spec.path(resource=transactionStop_res)
        spec.path(resource=metervalue_res)

        #print(json.dumps(spec.to_dict()))
        with open(SWAGGER_YAML_PATH, 'w') as file:
            file.write(json.dumps(spec.to_dict()))

        register_swaggerui_app(
            self, SWAGGERUI_URL, SCHEMA_URL,
            page_title=PAGE_TITLE,
            favicon_url=FAVICON_URL,
            config={'supportedSubmitMethods': ['get', 'post', 'put', 'patch'], }
        )


    def start(self):
        """ A hook to when a Gunicorn worker calls run()."""
        pass

    def stop(self, signal):
        """ A hook to when a Gunicorn worker starts shutting down. """
        pass


'''
class Provider(Schema):
    id = fields.Int(required=True)
    created_on = fields.Integer(required=True)
    updated_on = fields.Integer()
    name = fields.Str(required=True)
    wallet_id = fields.Int()
'''
