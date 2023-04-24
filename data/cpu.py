from .db_session import SqlAlchemyBase
import sqlalchemy


class Cpu(SqlAlchemyBase):
    __tablename__ = 'Cpus'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    power = sqlalchemy.Column(sqlalchemy.Integer)
