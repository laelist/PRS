import pymysql
from flask import Flask, request, redirect, render_template, url_for, session, flash
from app import app
from app.forms import LoginForm
# from flask_login import login_required


@app.route('/')
def home():
    print("!")
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('user', name=form.username.data))
    return render_template('login.html', form=form)


@app.route('/user/<name>/')
def user(name):
    return render_template('user.html', name=name, title=name + '的主页')



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
