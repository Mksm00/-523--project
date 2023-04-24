import flask
from flask import jsonify

from . import db_session
from .cpu import Cpu

blueprint = flask.Blueprint(
    'cpu_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/cpus')
def get_cpus():
    db_sess = db_session.create_session()
    cpus = db_sess.query(Cpu).all()
    return jsonify(
        {
            'cpus':
                [item.to_dict(only=('id', 'name', 'power'))
                 for item in cpus]
        }
    )


@blueprint.route('/api/cpus/<int:id>')
def get_cpu(id):
    db_sess = db_session.create_session()
    cpu = db_sess.query(Cpu).get(id)
    return jsonify(
        {
            'cpu':
                cpu.to_dict(only=('id', 'name', 'power'))
        }
    )
