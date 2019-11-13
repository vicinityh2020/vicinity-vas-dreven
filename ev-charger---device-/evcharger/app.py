import falcon

from evcharger.db import DBManager
from evcharger.middleware.context import ContextMiddleware
from evcharger.resources import evchargers


class DefaultService(falcon.API):
    def __init__(self, cfg):
        super(DefaultService, self).__init__(
            middleware=[ContextMiddleware()]
        )

        self.cfg = cfg

        # Build an object to manage our db connections.
        mgr = DBManager(self.cfg.db.connection)
        mgr.setup()

        # Create our resources
        evcharger_res = evchargers.EVchargersResource(mgr)

        # Build routes
        self.add_route('/objects', evcharger_res, suffix='TD')
        self.add_route('/objects/{oid}/properties/{pid}', evcharger_res)
        self.add_route('/infra', evcharger_res)


    def start(self):
        """ A hook to when a Gunicorn worker calls run()."""
        pass

    def stop(self, signal):
        """ A hook to when a Gunicorn worker starts shutting down. """
        pass

