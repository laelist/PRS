from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5


ao = db.Table(
    'AO',
    db.Column(
        'app_id',
        db.Integer,
        db.ForeignKey('applicant.app_id'),
        nullable=False),
    db.Column(
        'org_id',
        db.Integer,
        db.ForeignKey('organization.org_id'),
        nullable=False)
)

pe = db.Table(
    'PE',
    db.Column(
        'pro_id',
        db.Integer,
        db.ForeignKey('project.pro_id'),
        nullable=False),
    db.Column(
        'expert_id',
        db.Integer,
        db.ForeignKey('expert.expert_id'),
        nullable=False)
)


class User(UserMixin, db.Model):
    __tablename__ = 'user_t'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(
        db.String(20),
        index=True,
        nullable=False,
        unique=True)
    password = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return '<User {},{},{},{}>'.format(
            self.user_id,
            self.username,
            self.password,
            self.status
        )

    def set_password(self, pw):
        self.password = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    def get_id(self):
        return self.user_id

    def get_app_id(self):
        return Applicant.query.filter_by(user_id=self.get_id()).first().app_id

    def get_org_id(self):
        return Organization.query.filter_by(user_id=self.get_id()).first().org_id

    def get_expert_id(self):
        return Expert.query.filter_by(user_id=self.get_id()).first().expert_id

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.loli.net/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def org_app_pro_proclass():
    return Pro_class.query.join(
        Project, (Pro_class.class_id == Project.class_id)).add_entity(
        Project).join(
        Applicant, (Project.app_id == Applicant.app_id)).add_entity(
        Applicant).join(
        ao, (ao.c.app_id == Applicant.app_id)).join(
        Organization, (ao.c.org_id == Organization.org_id)).add_entity(
        Organization).order_by(
        Project.pro_id.desc())


class Project(db.Model):
    __tablename__ = 'project'
    pro_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pro_name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    expert_opinion = db.Column(db.String(100))
    pro_status = db.Column(db.String(1), nullable=False)
    pro_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    app_id = db.Column(
        db.Integer,
        db.ForeignKey('applicant.app_id'),
        nullable=False)
    class_id = db.Column(
        db.Integer,
        db.ForeignKey('pro_class.class_id'),
        nullable=False)

    def __repr__(self):
        return '<Project {},{},{},{},{},{},{},{}>'.format(
            self.pro_id,
            self.pro_name,
            self.email,
            self.expert_opinion,
            self.pro_status,
            self.pro_date,
            self.app_id,
            self.class_id
        )


class Organization(db.Model):
    __tablename__ = 'organization'
    org_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_name = db.Column(
        db.String(30),
        index=True,
        nullable=False,
        unique=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_t.user_id'),
        nullable=False)

    def __repr__(self):
        return '<Organization {},{}>'.format(
            self.org_id,
            self.org_name,
            self.user_id
        )

    def child_app(self):
        return Applicant.query.join(
            ao, (ao.c.app_id == Applicant.app_id)).filter(
            ao.c.org_id == self.org_id).order_by(
                    Applicant.app_name.asc())


class Applicant(db.Model):
    __tablename__ = 'applicant'
    app_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_name = db.Column(db.String(20), index=True, nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    professional = db.Column(db.String(20))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_t.user_id'),
        nullable=False)
    parent = db.relationship(
        'Organization', secondary=ao,
        primaryjoin=(ao.c.app_id == app_id),
        secondaryjoin=(ao.c.org_id == Organization.org_id),
        backref=db.backref('child', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Applicant {},{},{},{}>'.format(
            self.app_id,
            self.app_name,
            self.phone_number,
            self.professional
        )

    def parentd(self, org):
        if not self.is_parenting(org):
            self.parent.append(org)

    def unparentd(self, org):
        if self.is_parenting(org):
            self.parent.remove(org)

    def is_parenting(self, org):
        return self.parent.filter(
            ao.c.org_id == org.org_id).count() > 0

    def parented_org(self):
        return Organization.query.join(
            ao, (ao.c.org_id == Organization.org_id)).filter(
            ao.c.app_id == self.app_id).order_by(
                    Organization.org_name.asc())


class Expert(db.Model):
    __tablename__ = 'expert'
    expert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expert_name = db.Column(db.String(20), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_t.user_id'))
    expert_pro = db.relationship(
        'Project', secondary=pe,
        primaryjoin=(pe.c.expert_id == expert_id),
        secondaryjoin=(pe.c.pro_id == Project.pro_id),
        backref=db.backref('pro_expert'), lazy='dynamic')

    def __repr__(self):
        return '<Expert {},{},{}>'.format(
            self.expert_id,
            self.expert_name,
            self.user_id
        )


class Pro_information(db.Model):
    __tablename__ = 'pro_information'
    info_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    introduction = db.Column(db.String(500), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    pro_id = db.Column(db.Integer, db.ForeignKey(
        'project.pro_id'), nullable=False)

    def __repr__(self):
        return '<Pro_information {},{},{},{}>'.format(
            self.info_id,
            self.introduction,
            self.file_path,
            self.pro_id
        )


class Pro_class(db.Model):
    __tablename__ = 'pro_class'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(30), nullable=False)
    pro_class_name = db.Column(db.String(30), nullable=False, unique=True)
    start_time = db.Column(db.DateTime)
    over_time = db.Column(db.DateTime)
    exist_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False)
    department = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Pro_class {},{},{},{},{},{},{}>'.format(
            self.class_id,
            self.class_name,
            self.pro_class_name,
            self.start_time,
            self.over_time,
            self.exist_time,
            self.department
        )

