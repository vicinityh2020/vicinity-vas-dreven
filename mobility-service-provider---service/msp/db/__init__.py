import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping
from sqlalchemy_utils import database_exists, create_database

# Needed by the setup method as we want to make sure
# all models are loaded before we call create_all(...)
import msp.db.models


class DBManager(object):
    def __init__(self, connection=None):
        self.connection = connection

        self.engine = sqlalchemy.create_engine(self.connection)
        self.DBSession = scoping.scoped_session(
            orm.sessionmaker(
                bind=self.engine,
                autocommit=True
            )
        )

    @property
    def session(self):
        return self.DBSession()

    def setup(self):
        # Normally we would add whatever db setup code we needed here.
        # This will for fine for the ORM

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        try:
            models.BaseModel.metadata.create_all(self.engine)
        except Exception as e:
            print('Could not initialize DB: {}'.format(e))



