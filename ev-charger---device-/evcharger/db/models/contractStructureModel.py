import sqlalchemy as sa
from evcharger.db.models import BaseModel
import json



class ContractStructureModel(BaseModel):
    """
    This is the model that represents all possible structures for
    the contract definitions. Inherits every properties and functions
    from BaseModel and has the extra:
        Properties:
            -abi: Application Binary Interface (TEXT) -> (JSON)
            -bytecode: smart contract bytecode(TEXT) -> (JSON)
            -contract_type: refers to the type of contract
    """

    __tablename__ = 'contractStructures'
    CONTRACT_TYPE_STRING_SIZE = 128

    abi = sa.Column(sa.Text, nullable=False)
    bytecode = sa.Column(sa.Text, nullable=False)
    contract_type = sa.Column(sa.String(CONTRACT_TYPE_STRING_SIZE), unique=True)

    @property
    def as_dict(self):

        return {
            'abi': json.loads(self.abi),
            'bytecode': json.loads(self.bytecode),
            'contract_type': self.contract_type,
            **super(ContractStructureModel, self).as_dict
        }




