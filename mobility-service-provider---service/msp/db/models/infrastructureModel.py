import sqlalchemy as sa
import time
from msp.db.models import BaseModel
from msp.db.models import providerModel
from sqlalchemy.orm import relationship
from msp.utils.toTimestamp import to_timestamp, to_timestamp_ms
from datetime import datetime


class InfrastructureModel(BaseModel):
    """
    This is the model that represents providers Infrastructures. Inherits every
    properties and functions from BaseModel and has the extra:
        Properties:
            -provider_id: Foreign key of table providers
            -vicinity_oid: vicinity object id
            -last_start_transaction: timestamp from the last moment
                the charger starts charging
            -last_stop_transaction: timestamp from the last moment
                the charger stops charging
            -meterValue: amount of power consumpion
            -status: represents the infrastructure state
                True: occupied
                False: free to use
            -location: gps coordinates
    """

    __tablename__ = 'infrastructures'
    VICINITY_OID_STRING_SIZE = 128
    PROVIDER_MODEL_NAME = 'ProviderModel'
    PROVIDERS_ID_MODEL = 'providers.id'
    STATUS_STRING_SIZE = 128


    provider_id = sa.Column(sa.Integer, sa.ForeignKey(PROVIDERS_ID_MODEL), nullable=True)
    vicinity_oid = sa.Column(sa.String(VICINITY_OID_STRING_SIZE), unique=True, nullable=False)
    lastStartTransaction = sa.Column(sa.BigInteger, nullable=False,
                           default=to_timestamp_ms)
    lastStopTransaction = sa.Column(sa.BigInteger, nullable=False,
                           default=to_timestamp_ms)

    address = sa.Column(sa.String(STATUS_STRING_SIZE), nullable=True)
    name = sa.Column(sa.String(STATUS_STRING_SIZE), nullable=True)

    lastStartMeterValue = sa.Column(sa.Integer,  nullable=True)
    meterValue = sa.Column(sa.Integer,  nullable=True)
    status = sa.Column(sa.String(STATUS_STRING_SIZE), nullable=True)
    latitude =  sa.Column(sa.Float, nullable=True)
    longitude  = sa.Column(sa.Float, nullable=True)

    provider = relationship(PROVIDER_MODEL_NAME, backref=__tablename__)

    @property
    def as_dict(self):

        return {
            'name': self.name,
            'provider_id': self.provider_id,
            'vicinity_oid': self.vicinity_oid,
            'address': self.address,
            'lastStartTransaction': self.lastStartTransaction,
            'lastStopTransaction': self.lastStopTransaction,
            'lastStartMeterValue': self.lastStartMeterValue,
            'meterValue': self.meterValue,
            'status': self.status,
            'latitude': self.latitude,
            'longitude': self.longitude,
            **super(InfrastructureModel, self).as_dict
        }
