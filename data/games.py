from .db_session import SqlAlchemyBase
import sqlalchemy


class Games(SqlAlchemyBase):
    __tablename__ = 'Games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    developer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cpu = sqlalchemy.Column(sqlalchemy.Integer)
    card = sqlalchemy.Column(sqlalchemy.Integer)
    space = sqlalchemy.Column(sqlalchemy.Integer)
    op_space = sqlalchemy.Column(sqlalchemy.Integer)