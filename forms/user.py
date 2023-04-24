from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, SelectField, \
    IntegerField
from wtforms.validators import DataRequired, Length, number_range
from werkzeug.security import generate_password_hash, check_password_hash


class RegForm(FlaskForm):
    name = StringField('Введите логин', validators=[DataRequired(),
                                                    Length(min=8, max=16)])
    password = PasswordField('Введите пароль', validators=[DataRequired(),
                                                           Length(min=8, max=16)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(),
                                                                   Length(min=8, max=16)])
    email = StringField('Введите вашу почту', validators=[DataRequired()])
    submit = SubmitField()

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SearchForm(FlaskForm):
    genre = SelectField('Жанр:')
    developer = SelectField('Издатель:')
    year = SelectField('Год выпуска:')
    submit = SubmitField()


class ConfigForm(FlaskForm):
    id = IntegerField()
    cpu = SelectField('Видеокарта:', validators=[DataRequired()])
    card = SelectField('Процессор:', validators=[DataRequired()])
    space = IntegerField('Объем памяти накопителя:', validators=[DataRequired(), number_range(min=1)])
    op_space = IntegerField('Объем оперативной памяти:', validators=[DataRequired(), number_range(min=1)])
    submit = SubmitField('Сохранить')
