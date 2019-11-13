import sqlalchemy as sa
from evcharger.db.models import BaseModel
from evcharger.db.models import providerModel
from evcharger.db.models import endUserModel
from evcharger.db.models import contractStructureModel
from sqlalchemy.orm import relationship



class MultisigContractModel(BaseModel):
    """
    This is the model that represents contracts of type Multisig. Inherits every
    properties and functions from BaseModel and has the extra:
        Properties:
            -contract_structure_id: (Foreign key of table contractStructures)
            -provider_id: (Foreign key of table providers)
            -enduser_id: (Foreign key of table endusers)
            -address: address where contract is defined
    """

    __tablename__ = 'multisigContracts'
    ADDRESS_STRING_SIZE = 128

    CONTRACTSTRUCTURE_MODEL_NAME = 'ContractStructureModel'
    ENDUSER_MODEL_NAME ='EndUserModel'
    PROVIDER_MODEL_NAME = 'ProviderModel'

    CONTRACTSTRUCTURE_ID_MODEL = 'contractStructures.id'
    ENDUSER_ID_MODEL = 'endusers.id'
    PROVIDERS_ID_MODEL = 'providers.id'

    contract_structure_id = sa.Column(sa.Integer, sa.ForeignKey(CONTRACTSTRUCTURE_ID_MODEL), nullable=True)
    provider_id = sa.Column(sa.Integer, sa.ForeignKey(PROVIDERS_ID_MODEL), nullable=False)
    enduser_id = sa.Column(sa.Integer, sa.ForeignKey(ENDUSER_ID_MODEL), nullable=False)
    address = sa.Column(sa.String(ADDRESS_STRING_SIZE), nullable=False, unique=True)

    provider = relationship(PROVIDER_MODEL_NAME, backref=__tablename__)
    enduser = relationship(ENDUSER_MODEL_NAME, backref=__tablename__)
    contractStructure = relationship(CONTRACTSTRUCTURE_MODEL_NAME, backref=__tablename__)


    @property
    def as_dict(self):

        return {
            'contract_structure_id': self.contract_structure_id,
            'provider_id': self.provider_id,
            'enduser_id': self.enduser_id,
            'address': self.address,
            **super(MultisigContractModel, self).as_dict
        }





