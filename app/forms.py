from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired('账号不能为空')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登  陆')


class RegistrationForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired('账号不能为空')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    password2 = PasswordField(
        '再次输入密码',
        validators=[
            DataRequired('密码不能为空'),
            EqualTo('password', '两次密码不一致')])
    submit = SubmitField('注  册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已被使用')


class EditProfileForm(FlaskForm):
    app_name = StringField('姓名', validators=[DataRequired('姓名不能为空')])
    phone_number = StringField('电话号码', validators=[DataRequired('电话号码不能为空'), Length(11, 11, '电话号码不正确')])
    professional = StringField('职业')
    submit = SubmitField('提  交')
