import flask
from flask import jsonify

from . import db_session
from .games import Games

blueprint = flask.Blueprint(
    'games_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/games')
def get_games():
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    return jsonify(
        {
            'games':
                [item.to_dict(only=('id', 'name', 'year', 'genre', 'about', 'developer'))
                 for item in games]
        }
    )


@blueprint.route('/api/games/<int:id>')
def get_game(id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(id)
    return jsonify(
        {
            'game':
                game.to_dict(only=('id', 'name', 'year', 'genre', 'about', 'developer'))
        }
    )
