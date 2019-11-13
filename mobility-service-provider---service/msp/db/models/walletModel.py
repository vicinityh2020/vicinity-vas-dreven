import sqlalchemy as sa
from msp.db.models import BaseModel
from sqlalchemy.orm import relationship


class WalletModel(BaseModel):
    """
    This is the model that represents the Wallets. Inherits every
    properties and functions from BaseModel and has the extra:
        Properties:
            -string address: public address of wallet
    """

    __tablename__ = 'wallets'
    ADDRESS_STRING_SIZE = 128

    address = sa.Column(sa.String(ADDRESS_STRING_SIZE), unique=True, nullable=True)
    privKey = sa.Column(sa.String(ADDRESS_STRING_SIZE), unique=True, nullable=True)

    @property
    def as_dict(self):
        return {
            'address': self.address,
            'privKey': self.privKey,
            **super(WalletModel, self).as_dict
        }




