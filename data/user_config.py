from .db_session import SqlAlchemyBase
import sqlalchemy


class User_setup(SqlAlchemyBase):
    __tablename__ = 'Config'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    cpu = sqlalchemy.Column(sqlalchemy.String)
    card = sqlalchemy.Column(sqlalchemy.String)
    space = sqlalchemy.Column(sqlalchemy.Integer)
    op_space = sqlalchemy.Column(sqlalchemy.Integer)
