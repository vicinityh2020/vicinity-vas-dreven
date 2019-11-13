import sqlalchemy as sa
from msp.db.models import BaseModel
from msp.db.models import walletModel
from sqlalchemy.orm import relationship


class EndUserModel(BaseModel):
    """
    This is the model that represents the EndUsers. Inherits every
    properties and functions from BaseModel and has the extra:
        Properties:
            -string name
            -wallet_id:  (Foreign key of table wallets)
            -idTag: id from Magnums Cap charging car
            -email
            -pw
    """

    __tablename__ = 'endusers'
    NAME_TYPE_STRING_SIZE = 128
    EMAIL_TYPE_STRING_SIZE = 128
    PASSWORD_TYPE_STRING_SIZE = 128
    IDTAG_TYPE_STRING_SIZE = 128
    WALLET_MODEL_NAME = 'WalletModel'
    WALLET_ID_MODEL = 'wallets.id'

    name = sa.Column(sa.String(NAME_TYPE_STRING_SIZE))
    wallet_id = sa.Column(sa.Integer, sa.ForeignKey(WALLET_ID_MODEL), nullable=True)
    idTag = sa.Column(sa.String(IDTAG_TYPE_STRING_SIZE), unique=True)
    #meterValue = sa.Column(sa.Integer,  nullable=True)
    email = sa.Column(sa.String(EMAIL_TYPE_STRING_SIZE), unique=True)
    password = sa.Column(sa.String(PASSWORD_TYPE_STRING_SIZE))

    wallet = relationship(WALLET_MODEL_NAME, backref=__tablename__)

    @property
    def as_dict(self):

        return {
            'name': self.name,
            'wallet_id': self.wallet_id,
            'idTag': self.idTag,
            #'meterValue': self.meterValue,
            'email': self.email,
            'password': self.password,
            **super(EndUserModel, self).as_dict
        }





