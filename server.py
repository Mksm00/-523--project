from flask import Flask, url_for, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from data import db_session
from data.users import User
from data.games import Games
from data.user_config import User_setup
from data.cpu import Cpu
from data.card import Card
from forms.user import RegForm, LoginForm, SearchForm, ConfigForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a really really really really long secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base111.db'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/base111.db")
    app.run(port=8080, host='127.0.0.1', debug=True)


@app.route('/')
def nain():
    return render_template("index.html")


@app.route('/reg', methods=['POST', 'GET'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/enter')
    return render_template('register.html', title='Авторизация', form=form)


@app.route('/enter', methods=['GET', 'POST'])
def enter():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('enter.html',
                           message="Неправильный логин или пароль",
                           form=form)
    return render_template('enter.html', title='Авторизация', form=form)

@app.route('/browser', methods=['POST', 'GET'])
def browser():
    form = SearchForm()
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    games_genre = ['', 'RPG', 'Экшен', 'Симулятор', 'Приключения', 'Гонки', 'Шутер', 'Пазлы', 'Хоррор', 'Стратегия']
    games_developer = ['', 'Square Enix', 'Konami',
    'Microsoft', 'THQ', 'Rockstar Games', 'Red Barrels',
    'CD Projekt RED', 'GSC World Publishing', 'Mojang',
    'Ubisoft', 'Valve Software', 'Deep Silver', 'Electronic Arts',
    'Eidos Interactive', '4A Games', '2K Games', 'Bethesda Softworks',
    'Blizzard Entertainment', 'Activision', 'Warner Bros. Interactive Entertainment', 'Re-Logic', 'Capcom']
    games_year = ['', '1998', '1999', '2000', '2001', '2002', '2003',
                  '2004', '2005', '2006', '2007', '2008', '2009', '2010',
                  '2011', '2012', '2013', '2014', '2015', '2016', '2017',
                  '2018', '2019', '2020', '2021', '2022']
    form.genre.choices = games_genre
    form.developer.choices = games_developer
    form.year.choices = games_year
    if form.validate_on_submit():
        games = db_sess.query(Games).filter(Games.genre.like('%{}%'.format(form.genre.data)),
                                            Games.year.like('%{}%'.format(form.year.data)),
                                            Games.developer.like('%{}%'.format(form.developer.data)))
        return render_template('browser.html', games=games, form=form)
    return render_template('browser.html', games=games, form=form)

@app.route('/browser/<int:id>')
def game_page(id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(id)
    r_cpu = db_sess.query(Cpu.name).filter(Cpu.power == game.cpu).first()[0]
    r_card = db_sess.query(Card.name).filter(Card.power == game.card).first()[0]
    cui = int(current_user.get_id())
    if cui in [i.id for i in db_sess.query(User_setup).all()]:
        config = db_sess.query(User_setup).filter(User_setup.id == cui).first()
        us_cpu = int(db_sess.query(Cpu.power).filter(Cpu.name == config.cpu).first()[0])
        us_card = int(db_sess.query(Card.power).filter(Card.name == config.card).first()[0])
        print(us_cpu, us_card, config.space, config.op_space)
        print(game.cpu, game.card, game.space, game.op_space)
        if us_cpu >= game.cpu:
            cpu_yea = '+'
        else:
            cpu_yea = '-'
        if us_card >= game.card:
            card_yea = '+'
        else:
            card_yea = '-'
        if config.space >= game.space:
            space_yea = '+'
        else:
            space_yea = '-'
        if config.op_space >= game.op_space:
            op_space_yea = '+'
        else:
            op_space_yea = '-'

        print(cpu_yea, card_yea, space_yea, op_space_yea)

        return render_template('game_page.html', game=game, config=config, r_cpu=r_cpu, r_card=r_card,
                               cpu_yea=cpu_yea, card_yea=card_yea, space_yea=space_yea, op_space_yea=op_space_yea)
    else:
        config = db_sess.query(User_setup).filter(User_setup.id == cui).first()
        return render_template('game_page.html', game=game, config=config, r_cpu=r_cpu, r_card=r_card)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/config', methods=['POST', 'GET'])
@login_required
def set_config():
    form = ConfigForm()
    db_sess = db_session.create_session()
    list_cpu = [i.name for i in db_sess.query(Cpu).all()]
    form.cpu.choices = list_cpu
    list_card = [i.name for i in db_sess.query(Card).all()]
    form.card.choices = list_card
    cui = int(current_user.get_id())
    if form.validate_on_submit():
        if cui in [i.id for i in db_sess.query(User_setup).all()]:
            config = db_sess.query(User_setup).filter(User_setup.id == cui).first()
            config.cpu = form.cpu.data
            config.card = form.card.data
            config.space = form.space.data
            config.op_space = form.op_space.data
            db_sess.commit()
            return redirect('/browser')
        else:
            db_sess = db_session.create_session()
            config = User_setup(id=cui, cpu=form.cpu.data, card=form.card.data, space=form.space.data, op_space=form.op_space.data)
            db_sess.add(config)
            db_sess.commit()
            return redirect('/browser')
    return render_template('config.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        main()
