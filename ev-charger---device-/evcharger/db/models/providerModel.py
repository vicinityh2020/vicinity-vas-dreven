import sqlalchemy as sa
from evcharger.db.models import BaseModel
from evcharger.db.models import walletModel
from sqlalchemy.orm import relationship


class ProviderModel(BaseModel):
    """
    This is the model that represents the Providers. Inherits every
    properties and functions from BaseModel and has the extra:
        Properties:
            -string name
            -wallet_id  (Foreign key of table wallets)
    """

    __tablename__ = 'providers'
    NAME_STRING_SIZE = 128

    WALLET_MODEL_NAME = 'WalletModel'
    WALLET_ID_MODEL = 'wallets.id'

    name = sa.Column(sa.String(NAME_STRING_SIZE), unique=True)
    wallet_id = sa.Column(sa.Integer, sa.ForeignKey(WALLET_ID_MODEL), nullable=True)

    wallet = relationship(WALLET_MODEL_NAME, backref=__tablename__)

    @property
    def as_dict(self):
        return {
            'name': self.name,
            'wallet_id': self.wallet_id,
            **super(ProviderModel, self).as_dict
        }





