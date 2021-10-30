import os
import uuid

from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db, moment
from app.forms import LoginForm, RegistrationForm, EditAppProfileForm, EditOrgProfileForm, EditProjectClassForm, \
    EditProjectForm
from app.models import User, Applicant, Organization, Pro_class, Project, Pro_information, app_pro_proclass

app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/test/<name>', methods=['GET', 'POST'])
def test(name):
    user = User.query.filter_by(username=name).first_or_404()
    form = EditProjectForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = random_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_PATH'], user.username)
        print(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        if f.save(os.path.join(path, filename)):
            flash('文件上传成功')
        else:
            flash('文件上传失败')
        return redirect(url_for('test', name=name))
    return render_template("test.html", name=name, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_home_page', name=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.status = 'a'
        db.session.add(user)
        db.session.commit()
        # db.session.close()
        flash('注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_home_page', name=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('错误的账号或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user_home_page', name=form.username.data)
        return redirect(next_page)
    return render_template('login.html', title='项目评审管理登陆', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<name>/home/')
@login_required
def user_home_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    return render_template('userHome.html', user=user, title=name + '的主页')


@app.route('/user/<name>/project/', methods=['GET', 'POST'])
@login_required
def user_project_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    page = request.args.get('page', 1, type=int)
    print(app_pro_proclass().all())
    project = app_pro_proclass().paginate(
        page, app.config['PROJECT_PER_PAGE'], False)
    next_url = url_for(
        'user_project_page',
        page=project.next_num,
        name=name) if project.has_next else None
    prev_url = url_for(
        'user_project_page',
        page=project.prev_num,
        name=name) if project.has_prev else None
    return render_template(
        'userProject.html',
        user=user,
        title=name + '的项目',
        project=project,
        next_url=next_url,
        prev_url=prev_url)


@app.route('/user/<name>/projectclass/')
@login_required
def user_projectclass_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    page = request.args.get('page', 1, type=int)
    proclass = Pro_class.query.order_by(Pro_class.class_id.desc()).paginate(
        page, app.config['PROJECT_PER_PAGE'], False)
    next_url = url_for(
        'user_projectclass_page',
        page=proclass.next_num,
        name=name) if proclass.has_next else None
    prev_url = url_for(
        'user_projectclass_page',
        page=proclass.prev_num,
        name=name) if proclass.has_prev else None
    return render_template(
        'projectClass.html',
        user=user,
        title='项目类',
        proclass=proclass,
        next_url=next_url,
        prev_url=prev_url)


# done：2完成表单 3完成ap关系绑定
@app.route('/applicant/<name>/newproject/', methods=['GET', 'POST'])
@login_required
def applicant_newproject_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    form = EditProjectForm()
    if form.validate_on_submit():
        project = Project(
            pro_name=form.pro_name.data,
            email=form.email.data,
            pro_status='d',
            app_id=current_user.get_app_id(),
            class_id=form.class_id.data)
        f = form.file.data
        filename = random_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_PATH'], current_user.username)
        print(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        fpath = os.path.join(path, filename)
        f.save(fpath)
        flash('上传成功')
        db.session.add(project)
        db.session.commit()
        pro_id = Project.query.filter_by(pro_name=form.pro_name.data).first().pro_id
        pro_info = Pro_information(
            introduction=form.introduction.data,
            file_path=fpath,
            pro_id=pro_id
        )
        db.session.add(pro_info)
        db.session.commit()
        return redirect(url_for('applicant_newproject_page', name=name))
    return render_template(
        'applicantNewProject.html',
        user=user,
        title=name + '的新建项目',
        form=form)


# todo：4实现状态转换以及二次编辑功能
#   状态转换可考虑disable属性，类似{{ if project.status != 'd' }} disable {{ endif }}
@app.route('/applicant/<name>/editproject/<pro_id>', methods=['GET', 'POST'])
@login_required
def applicant_editproject_page(name, pro_id):
    user = User.query.filter_by(username=name).first_or_404()
    project = Project.query.filter_by(pro_id=pro_id).first()
    if current_user.status == 'a' and project is not None:
        form = EditProjectForm()
        if form.validate_on_submit():
            # todo:处理返回的信息
            pass
        elif request.method == 'GET':
            # todo:获取项目信息赋到表中
            pass
        return render_template('accesslimit.html')
    return render_template('accesslimit.html')


@app.route('/applicant/<name>/profile/', methods=['GET', 'POST'])
@login_required
def applicant_profile_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    form = EditAppProfileForm()
    if form.validate_on_submit():
        applicant = Applicant.query.filter_by(
            user_id=current_user.user_id).first()
        if applicant is None:
            applicant = Applicant(user_id=current_user.user_id)
        applicant.app_name = form.app_name.data
        applicant.phone_number = form.phone_number.data
        applicant.professional = form.professional.data
        db.session.add(applicant)
        db.session.commit()
        # db.session.close()
        flash('修改已保存')
        return redirect(url_for('applicant_profile_page', name=name))
    elif request.method == 'GET':
        applicant = Applicant.query.filter_by(
            user_id=current_user.user_id).first()
        if applicant is not None:
            form.app_name.data = applicant.app_name
            form.phone_number.data = applicant.phone_number
            form.professional.data = applicant.professional
    return render_template(
        'applicantProfile.html',
        user=user,
        title=name + '的个人信息',
        form=form)


@app.route('/applicant/<name>/parent/', methods=['GET', 'POST'])
@login_required
def applicant_parent_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    applicant = Applicant.query.filter_by(user_id=current_user.user_id).first()
    po = applicant.parented_org().all()
    return render_template(
        'applicantParent.html',
        user=user,
        title=name + '的所属公司',
        po=po,
        applicant=applicant)


# todo：1.0.9实现公司的项目提交功能


@app.route('/organization/<name>/profile/', methods=['GET', 'POST'])
@login_required
def organization_profile_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    form = EditOrgProfileForm()
    if form.validate_on_submit():
        org = Organization.query.filter_by(
            user_id=current_user.user_id).first()
        if org is None:
            org = Organization(user_id=current_user.user_id)
        org.org_name = form.org_name.data
        db.session.add(org)
        db.session.commit()
        # db.session.close()
        flash('修改已保存')
        return redirect(url_for('organization_profile_page', name=name))
    elif request.method == 'GET':
        org = Organization.query.filter_by(
            user_id=current_user.user_id).first()
        if org is not None:
            form.org_name.data = org.org_name
    return render_template(
        'organizationProfile.html',
        user=user,
        title=name + '的公司信息',
        form=form)


@app.route('/organization/<name>/child/', methods=['GET', 'POST'])
@login_required
def organization_child_page(name):
    user = User.query.filter_by(username=name).first_or_404()
    organization = Organization.query.filter_by(
        user_id=current_user.user_id).first()
    page = request.args.get('page', 1, type=int)
    po = organization.child_app().paginate(
        page, app.config['PROJECT_PER_PAGE'], False)
    next_url = url_for(
        'organization_child_page',
        page=po.next_num,
        name=name) if po.has_next else None
    prev_url = url_for(
        'organization_child_page',
        page=po.prev_num,
        name=name) if po.has_prev else None

    return render_template(
        'organizationChild.html',
        user=user,
        title=name + '的员工表',
        po=po,
        organization=organization,
        next_url=next_url,
        prev_url=prev_url)


# todo：1.1.0专家页面，需实现项目评审的评审功能


@app.route('/admin/<name>/tools/', methods=['GET', 'POST'])
@login_required
def admin_page(name):
    if current_user.status == 's':
        user = User.query.filter_by(username=name).first_or_404()
        return render_template(
            'adminTools.html',
            user=user,
            title=name + '的管理空间')
    return render_template('accesslimit.html')


@app.route('/admin/<name>/newclass/', methods=['GET', 'POST'])
@login_required
def admin_newclass_page(name):
    if current_user.status == 's':
        user = User.query.filter_by(username=name).first_or_404()
        form = EditProjectClassForm()
        if form.validate_on_submit():
            proclass = Pro_class()
            proclass.class_name = form.class_name.data
            proclass.pro_class_name = form.pro_class_name.data
            proclass.over_time = form.over_time.data
            proclass.start_time = form.start_time.data
            proclass.department = form.department.data
            print(proclass)
            db.session.add(proclass)
            db.session.commit()
            flash('修改已保存')
            return redirect(url_for('admin_newclass_page', name=name))
        return render_template(
            'adminNewclass.html',
            user=user,
            title=name + '的新建类',
            form=form)
    return render_template('accesslimit.html')
