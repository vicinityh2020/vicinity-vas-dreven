import time
import sqlalchemy as sa
from datetime import datetime
from evcharger.utils.toTimestamp import to_timestamp, to_timestamp_ms
from sqlalchemy.ext.declarative import declarative_base
SAModel = declarative_base()


class BaseModel(SAModel):
    """
    BaseModel is the super for every other model in this solution
    Every entry on DB has:
        Properties:
            -integer id
            -DateTime registed_on, updated_on

        Functions:
            -get_by_id(cls, session, _id) - get object of _id DB entry
            -get_generic(cls, session, **kwargs) - filter entry by generic input
                through **kwargs
            -get_all(cls, session) - get list of all entries
            -as_dict(self) - get dictionary with id, registed_on and updated_on
            -save(self, session) - save entry to DB
            -update(self, session, **kwargs) - update entry with received kwargs

    """

    __abstract__ = True

    @classmethod
    def get_by_id(cls, session, _id):
        """
        Returns model with specified _id
        """
        with session.begin():
            obj = session.query(cls).get(_id)
            return obj if obj else None

    @classmethod
    def get_generic(cls, session, **kwargs):
        """
        Returns a list of models filtered by the provided key words
        """
        with session.begin():
            obj = session.query(cls).filter_by(**kwargs).all()
            return obj if obj else None

    @classmethod
    def get_all(cls, session):
        with session.begin():
            query = session.query(cls)
            models = query.all()

        return models

    @property
    def as_dict(self):
        """
        Returns __obj with {id, registed_on, updated_on] after converting
        DateTime types to timestamps using function to_timestamp() in
        defined in utils folder
        """

        __obj = {
            'registered_on': self.created_on,
            'id': self.id
            }
        if self.updated_on:
            __obj['updated_on'] = self.updated_on

        return __obj

    def save(self, session):
        with session.begin():
            session.add(self)

    def update(self, session, **kwargs):
        with session.begin():
            for k,v in kwargs.items():
                setattr(self, k, v)


    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_on = sa.Column(sa.BigInteger, nullable=False,
                           default=to_timestamp_ms)
    updated_on = sa.Column(sa.BigInteger, nullable=True,
                            onupdate=to_timestamp_ms)

