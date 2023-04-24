import flask
from flask import jsonify

from . import db_session
from .card import Card

blueprint = flask.Blueprint(
    'card_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/cards')
def get_cards():
    db_sess = db_session.create_session()
    cards = db_sess.query(Card).all()
    return jsonify(
        {
            'cards':
                [item.to_dict(only=('id', 'name', 'power'))
                 for item in cards]
        }
    )


@blueprint.route('/api/cards/<int:id>')
def get_card(id):
    db_sess = db_session.create_session()
    card = db_sess.query(Card).get(id)
    return jsonify(
        {
            'card':
                card.to_dict(only=('id', 'name', 'power'))
        }
    )
