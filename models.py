from flask_login import UserMixin
from app import db
import pytz
from datetime import datetime



IST = pytz.timezone('Asia/Kolkata')
x = datetime.now(IST)
time = x.strftime("%c")

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    users = db.relationship('Users', cascade="all,delete", backref='user')
    certificates = db.relationship(
        'Certificate', cascade="all,delete", backref='student')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    profile_image = db.Column(db.String(500), nullable=True)
    status = db.Column(db.Integer, nullable=False)
    lastlogin = db.Column(db.String(50), nullable=False)
    is_staff = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    createddate = db.Column(db.String(50), nullable=False)
    orgid = db.Column(db.Integer, db.ForeignKey(
        'organization.id'), nullable=True)
    certificate = db.relationship(
        'Certificate', cascade="all,delete", backref='certificate')


class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_num = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    qr_code = db.Column(db.String(100), nullable=True)


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    coursename = db.Column(db.String(500), nullable=False)
    dateupdate = db.Column(db.String(50), nullable=False)
    createddate = db.Column(db.String(50), nullable=False)
    orgid = db.Column(db.Integer, db.ForeignKey('organization.id'))
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))


class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    ip = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50), nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    ip = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50), nullable=False)


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    email = db.Column(db.String(127), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    order_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    payment_id = db.Column(db.String(127), nullable=False)
    response_msg = db.Column(db.Text(), nullable=False)
    status = db.Column(db.String(25), nullable=False)
    error_code = db.Column(db.String(127), nullable=True)
    error_source = db.Column(db.String(127), nullable=True)
    txn_timestamp = db.Column(
        db.DateTime(), default=datetime.now(IST), nullable=False)
