from .db_session import SqlAlchemyBase
import sqlalchemy


class Card(SqlAlchemyBase):
    __tablename__ = 'Gcards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    power = sqlalchemy.Column(sqlalchemy.Integer)
