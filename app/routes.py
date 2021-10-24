import pymysql
from flask import Flask, request, redirect, render_template, url_for, session, flash
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_page', name=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.status = 'a'
        db.session.add(user)
        db.session.commit()
        flash('注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_page', name=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('错误的账号或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user_page', name=form.username.data)
        return redirect(next_page)
    return render_template('login.html', title='项目评审管理登陆', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<name>/home')
@login_required
def user_page(name):
    return render_template('user.html', name=name, title=name + '的主页')


@app.route('/user/<name>/project')
@login_required
def user_project_page(name):
    return render_template('userProject.html', name=name, title=name + '的项目')

# def logindata(username, password):
#     db = pymysql.connect(
#         host='127.0.0.1',
#         user='chao',
#         password='235711',
#         database='project_review',
#         charset='utf8')
#     # 得到游标
#     cursor = db.cursor()
#
#     sql = 'select status from user_t where username=\'%s\' and password=\'%s\'' % (
#         username, password)
#     # 执行SQL
#     cursor.execute(sql)
#     # 获取数据
#     data = cursor.fetchall()
#     return data
#
#
# def check():
#     return session.get('access')
#
#
# @app.route('/')
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = ''
#     if request.method == 'POST':
#         if request.form['exampleInputUser1']:
#             if request.form['exampleInputPassword1']:
#                 username = request.form['exampleInputUser1']
#                 pw = request.form['exampleInputPassword1']
#                 status = logindata(username, pw)
#                 if status:
#                     session['username'] = username
#                     session['access'] = status[0][0]
#                     # st = hashlib.md5(pw.encode(encoding='UTF-8')).hexdigest()
#                     return redirect(url_for('user', name=username))
#                 else:
#                     error = '账号密码不匹配'
#             else:
#                 error = '错误的密码'
#         else:
#             error = '错误的账号'
#
#     return render_template('main.html', error=error)
#
#
# @app.route('/user/<name>/')
# def user(name):
#     if check():
#         if check() == 'a':
#             pass
#         elif check() == 'e':
#             pass
#         elif check() == 'o':
#             pass
#         elif check() == 's':
#             pass
#     else:
#         error = '请重新登陆'
#         return render_template('main.html', error=error)
#
#     return render_template('user.html', name=name, title=name + '的主页')
