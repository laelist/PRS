from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from app.models import User, Pro_class


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


class EditAppProfileForm(FlaskForm):
    app_name = StringField('姓名', validators=[DataRequired('姓名不能为空')])
    phone_number = StringField('电话号码', validators=[DataRequired('电话号码不能为空'), Length(11, 11, '电话号码不正确')])
    professional = StringField('职业')
    submit = SubmitField('提  交')


class EditOrgProfileForm(FlaskForm):
    org_name = StringField('公司名称', validators=[DataRequired('公司名不能为空')])
    submit = SubmitField('提  交')


class EditProjectClassForm(FlaskForm):
    class_name = StringField('类别', validators=[DataRequired('类别不能为空')])
    pro_class_name = StringField('项目类型', validators=[DataRequired('项目类型不能为空')])
    over_time = StringField('截止时间')
    start_time = StringField('开始时间')
    department = StringField('立项部门', validators=[DataRequired('立项部门不能为空')])
    submit = SubmitField('提  交')

    def validate_pro_class_name(self, pro_class_name):
        proclass = Pro_class.query.filter_by(pro_class_name=pro_class_name.data).first()
        if proclass is not None:
            raise ValidationError('项目类型已存在！')


class EditProjectForm(FlaskForm):
    pro_name = StringField('项目名称', validators=[DataRequired('项目名称不能为空')])
    email = StringField('联系邮箱', validators=[DataRequired('联系邮箱不能为空')])
    # app_opinion = StringField('专家意见', Length(0, 100, '不能超过100字'))
    # app_status = StringField('项目建立时间')
    introduction = StringField('项目简介', validators=[DataRequired('简介不能为空'), Length(0, 500, '不能超过500字')])
    file = StringField('附件', validators=[DataRequired('附件不能为空')])
    submit = SubmitField('提  交')