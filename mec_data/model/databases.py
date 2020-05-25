from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.pool import NullPool


class SQLAlchemy(SQLAlchemyBase):
    def apply_driver_hacks(self, app, info, options):
        super(SQLAlchemy, self).apply_driver_hacks(app, info, options)
        options['poolclass'] = NullPool
        options.pop('pool_size', None)


data_warehouse = SQLAlchemy()
