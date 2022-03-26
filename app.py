from multiprocessing.pool import ThreadPool
import os
import threading
from flask.globals import current_app
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, render_template, redirect, request, flash, url_for, jsonify, abort, send_from_directory, make_response
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from password_generator import PasswordGenerator
from flask_mail import Mail, Message
from datetime import datetime
import json as json_lib
import requests
import random
import string
import pytz
import re
import razorpay
import hmac
import hashlib
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
import qrcode
from flask_login import UserMixin
from functools import wraps
from decouple import config
import csv
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_migrate import Migrate
import io
from flask_cors import CORS

# AWS S3 Bucket
import boto3
# Facebook Login
# import requests_oauthlib
# from requests_oauthlib.compliance_fixes import facebook_compliance_fix
# Pdf Conversion
# import pdfkit


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

# SES Conf
CHARSET = "UTF-8"


def check(email):
    return re.search(regex, email)


# end

app = Flask(__name__)
CORS(app, resources={r"v1/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(config("app_settings"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('email_username')
app.config['MAIL_PASSWORD'] = config('email_password')
app.config['MAIL_DEBUG'] = False

app.config.from_object(config("app_settings"))


db = SQLAlchemy(app)
mail = Mail(app)


if db.engine.url.drivername == 'sqlite':
    migrate = Migrate(app, db, render_as_batch=True)
else:
    migrate = Migrate(app, db)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# serializer for registration
s = URLSafeTimedSerializer(app.secret_key)


login_manager = LoginManager(app)
login_manager.login_view = 'loginPage'
login_manager.login_message_category = 'info'

RAZORPAY_KEY_ID = config("razorpay_key_id")
RAZORPAY_KEY_SECRET = config("razorpay_key_secret")

# S3 Client
# s3_client = boto3.client('s3', aws_access_key_id=config(
#     "S3_KEY"), aws_secret_access_key=config("S3_SECRET_ACCESS_KEY"))

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET")
)


def upload(file, **options):
    res = cloudinary.uploader.upload(file)
    return res['secure_url']


# Facebook Login Credentials
# FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
# FB_TOKEN_URL = config('facebook_token_url')
# FB_CLIENT_ID = config("facebook_app_id")
# FB_CLIENT_SECRET = config("facebook_secret")

# Google Login Credentials
GOOGLE_CLIENT_ID = config("google_client_id")
GOOGLE_CLIENT_SECRET = config("google_client_secret")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

IST = pytz.timezone('Asia/Kolkata')
x = datetime.now(IST)
time = x.strftime("%c")
host = config('host_status', default=False, cast=bool)
ipc = config("demo_ip")
favTitle = config("favTitle")
site_url = config("site_url")


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    profile_image = db.Column(db.String(500), nullable=True)
    status = db.Column(db.Integer, nullable=False)
    is_staff = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.String(50), nullable=False)
    group = db.relationship('Group', cascade="all,delete", backref='group')


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    token_id = db.Column(db.String(200), nullable=False)
    # U->Used, E->Expired, A->Available
    status = db.Column(db.String(50), nullable=False, default='A')


class Fonts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    font_cdn = db.Column(db.String(500), nullable=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    textColor = db.Column(db.String(50), nullable=True)
    bg_image = db.Column(db.String(500), nullable=True)
    font_size = db.Column(db.Integer, nullable=False)
    font_name = db.Column(db.String(250), nullable=False)
    certx = db.Column(db.Integer, nullable=False)
    certy = db.Column(db.Integer, nullable=False)
    qrx = db.Column(db.Integer, nullable=False)
    qry = db.Column(db.Integer, nullable=False)
    certnox = db.Column(db.Integer, nullable=False)
    certnoy = db.Column(db.Integer, nullable=False)
    prefix = db.Column(db.String(20), default='CGV')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    certificates = db.relationship(
        'Certificate', cascade="all,delete", backref='certificates')


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    is_email_sent = db.Column(db.Boolean, default=False)
    coursename = db.Column(db.String(500), nullable=False)
    last_update = db.Column(db.String(50), nullable=False, default=x)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    qrcode = db.relationship('QRCode', cascade="all,delete", backref='qrcode')


class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_num = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    qr_code = db.Column(db.String(100), nullable=True)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'))


class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
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


class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    group_name = db.Column(db.String(50), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    usage_limit = db.Column(db.Integer, nullable=True)
    is_valid = db.Column(db.Boolean, nullable=False, default=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    date_generated = db.Column(db.String(50), nullable=False)


class PublicAPIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(50), nullable=False)
    is_valid = db.Column(db.Boolean, nullable=False, default=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    date_generated = db.Column(db.String(50), nullable=False)


# Admin Required Decorator

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_staff:
            flash('You are not authorized to access this page.', 'danger')
            return render_template('block.html', favTitle=favTitle, user=current_user)
        return func(*args, **kwargs)
    return decorated_view


# Use if Sendgrid is configured

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#         return True

# def send_email_now(email, subject, from_email, from_email_name, template_name, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message(
#         sender=(from_email_name, from_email),
#         recipients=[email],
#         subject=subject
#     )
#     msg.html = render_template(template_name, **kwargs)
#     try:
#         thr = threading.Thread(target=send_async_email, args=[app, msg]).start()
#         return thr
#     except Exception as e:
#         print(e)
#         return False

def send_async_email(app, client, data):
    with app.app_context():
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    data["email"],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': data["msg_html"],
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': data["subject"],
                },
            },
            Source=data["sender"],
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]


def send_email_now(email, subject, from_email, from_email_name, template_name, **kwargs):
    aws_email = config("AWS_SES_VERIFIED_EMAIL")
    sender = f"{from_email_name} <{aws_email}>"
    client = boto3.client('ses',
                          region_name=config("AWS_REGION"),
                          aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=config("AWS_ACCESS_KEY_SECRET")
                          )
    msg_html = render_template(template_name, **kwargs)
    data = {
        "email": email,
        "subject": subject,
        "sender": sender,
        "msg_html": msg_html
    }
    try:
        pool = ThreadPool(processes=1)
        # Provide the contents of the email.
        async_res = pool.apply_async(send_async_email, [app, client, data])
        return async_res.get() == 200
    # Display an error if something goes wrong.
    except Exception as e:
        print(e)
        return False


# def upload_image(file, bucket="cgv", **kwargs):
#     """
#     Function to upload an image to an S3 bucket
#     """
#     if kwargs["folder"] == "qr_codes":
#         response = s3_client.put_object(
#             Bucket=bucket,
#             Key=f'{kwargs["folder"]}/{kwargs["number"]}.png',
#             Body=file,
#             ContentType='image/png',
#         )
#     else:
#         response = s3_client.put_object(
#             Bucket=bucket,
#             Key=f'{kwargs["folder"]}/{kwargs["name"]}',
#             Body=file,
#             ContentType='image/png',
#         )

#     return response


# def upload_doc(file, bucket="cgv", **kwargs):
#     """
#     Function to upload a raw file to an S3 bucket
#     """
#     if kwargs["localhost"]:
#         with open(file, "rb") as f:
#             response = s3_client.upload_fileobj(
#                 f, bucket, f'certificates/{kwargs["number"]}.pdf')
#     else:
#         response = s3_client.put_object(
#             Bucket=bucket,
#             Key=f'certificates/{kwargs["number"]}.pdf',
#             Body=file,
#         )

#     return response


# def delete_from_s3(file, bucket='cgv'):
#     """
#     Function to delete objects from S3 bucket
#     """
#     s3_client.delete_object(Bucket=bucket, Key=file)

# For Gravatar


def avatar(email, size):
    digest = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


def send_password_reset_email(name, email):
    token = s.dumps(email, salt='cgv-password-reset')
    new_token = Token(email=email, token_id=token, status='A')
    db.session.add(new_token)
    db.session.commit()
    if app.debug:
        link = f"http://127.0.0.1:5000/reset-password/{token}"
    else:
        link = f"{config('site_url')}/reset-password/{token}"
    print(link)
    subject = "Password Reset Link | CGV"
    return send_email_now(email, subject, 'password-bot@cgv.in.net', 'Password Bot CGV', 'emails/reset-password.html', name=name, link=link)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password_page():
    if (request.method == 'POST'):
        email = request.form.get('email')
        post = Users.query.filter_by(email=email).first()
        name = post.name
        if (post != None):
            if (post.email == config("admin_email")):
                flash("You can't reset password of administrator!", "danger")
            else:
                if send_password_reset_email(name, email):
                    flash(
                        f"We've sent a password reset link on {email}", "success")
                else:
                    flash("Error while sending password reset email!", "danger")
        elif (post == None):
            flash("We didn't find your account!", "danger")
            return render_template('forgot-password.html', favTitle=favTitle, verified=False)

    return render_template('forgot-password.html', favTitle=favTitle, verified=False)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    if request.method == 'POST':
        password = request.form.get('password')
        password = sha256_crypt.hash(password)
        email = s.loads(token, salt="cgv-password-reset")
        user = Users.query.filter_by(email=email).first()
        user.password = password
        db_token = Token.query.filter_by(token_id=token).first()
        db_token.status = 'U'
        db.session.commit()
        flash('Password changed successfully.', 'success')
        return redirect(url_for('loginPage'))
    try:
        email = s.loads(token, salt="cgv-password-reset", max_age=1800)
    except SignatureExpired:
        db_token = Token.query.filter_by(token_id=token).first()
        db_token.status = 'E'
        db.session.commit()
        flash("Sorry, link has been expired.", "danger")
        return render_template('forgot-password.html', favTitle=favTitle, verified=False)
    except Exception:
        flash("Sorry, Invalid token.", "danger")
        return render_template('forgot-password.html', favTitle=favTitle, verified=False)
    user = Users.query.filter_by(email=email).first()
    first_name = user.name.split(" ")[0]
    db_token = Token.query.filter_by(token_id=token).first()
    if db_token.status == 'U':
        flash("Sorry, link has been already used.", "danger")
        return render_template("forgot-password.html", favTitle=favTitle, name=first_name, token=token, verified=False)
    elif db_token.status == 'E':
        flash("Sorry, link has been expired.", "danger")
        return render_template("forgot-password.html", favTitle=favTitle, name=first_name, token=token, verified=False)
    return render_template("forgot-password.html", favTitle=favTitle, name=first_name, token=token, verified=True)


@app.route('/')
def home_page():
    try:
        response = requests.get(config("contributors_api"))
        team = response.json()
    except Exception:
        team = {}
    return render_template('index.html', favTitle=favTitle, team=team, user=current_user)


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('editordata')
        if (host == True):
            try:
                ip_address = request.environ['HTTP_X_FORWARDED_FOR']
            except KeyError:
                ip_address = request.remote_addr
            except Exception:
                ip_address = ipc
        else:
            ip_address = ipc
        # name validation it must be greater than than 2 letters and less than 40 letters
        if len(name) >= 2 and len(name) <= 40:
            pass
        else:
            flash("Please Enter Your Name Correctly!! ", "danger")
            return redirect("/#footer")
        # email validation
        if check(email):
            pass
        else:
            flash(
                "Email is not Correct Please Check it and Try It once again!!", "danger")
            return redirect('/#footer')
        # number validation
        if len(phone) >= 8 and len(phone) <= 13:
            pass
        else:
            flash(
                "Phone Number is not Correct Please Check it and Try It once again!!", "danger")
            return redirect('/#footer')
        entry = Contact(name=name, phone=phone, message=message, ip=ip_address, date=time,
                        email=email)
        db.session.add(entry)
        db.session.commit()
        flash("Thank you for contacting us – we will get back to you soon!", "success")
    return redirect('/#footer')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if (request.method == 'POST'):
        data = json_lib.loads(request.data)
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        rating = data["rating"]
        message = data["message"]
        if (host == True):
            try:
                ip_address = request.environ['HTTP_X_FORWARDED_FOR']
            except KeyError:
                ip_address = request.remote_addr
            except Exception:
                ip_address = ipc
        else:
            ip_address = ipc
        try:
            entry = Feedback(name=name, phone=phone, rating=rating,
                             message=message, ip=ip_address, date=time, email=email)
            db.session.add(entry)
            db.session.commit()
            return jsonify(feedback_success="Thank you for feedback – we will get back to you soon!", status=200)
        except Exception:
            return jsonify(feedback_error="Sorry, we could not record your feedback.", status=400)
    return redirect('/#footer')


@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter_page():
    if (request.method == 'POST'):
        email = request.form.get('email')
        if (host == True):
            try:
                ip_address = request.environ['HTTP_X_FORWARDED_FOR']
            except KeyError:
                ip_address = request.remote_addr
            except Exception:
                ip_address = ipc
        else:
            ip_address = ipc
        post = Newsletter.query.filter_by(email=email).first()
        if (post == None):
            entry = Newsletter(ip=ip_address, date=time, email=email)
            db.session.add(entry)
            db.session.commit()
            flash("Thank you for subscribing!", "success")
        else:
            flash("You have already subscribed!", "danger")
    return redirect('/#footer')


@app.route("/certificate/verify", methods=['GET', 'POST'])
def certificate_verify():
    if (host == True):
        try:
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        except KeyError:
            ip_address = request.remote_addr
        except Exception:
            ip_address = ipc
    else:
        ip_address = ipc
    if (request.method == 'POST'):
        certificate_no = request.form.get('certificateno')
        postc = Certificate.query.filter_by(number=certificate_no).first()
        if (postc != None):
            posto = Group.query.filter_by(id=postc.group_id).first()
            flash("Certificate Number Valid!", "success")
            return render_template('Redesign-verify2.html', postc=postc, posto=posto, favTitle=favTitle, ip=ip_address)
        elif (postc == None):
            flash("No details found. Contact your organization!", "danger")
    return render_template('Redesign-verify2.html', favTitle=favTitle, ip=ip_address, user=current_user)


# @app.route("/certificate/generate", methods=['GET', 'POST'])
# def certificate_generate():
#     if (host == True):
#         try:
#             ip_address = request.environ['HTTP_X_FORWARDED_FOR']
#         except KeyError:
#             ip_address = request.remote_addr
#         except Exception:
#             ip_address = ipc
#     else:
#         ip_address = ipc
#     if (request.method == 'POST'):
#         certificateno = request.form.get('certificateno')
#         postc = Certificate.query.filter_by(number=certificateno).first()
#         if (postc != None):
#             posto = Group.query.filter_by(id=postc.group_id).first()
#             qr_code = QRCode.query.filter_by(
#                 certificate_num=certificateno).first()
#             img_url = qr_code.qr_code
#             rendered_temp = render_template('certificate.html', postc=postc, posto=posto,
#                                             qr_code=img_url, favTitle=favTitle, site_url=site_url, number=certificateno, pdf=True)
#             if not app.debug:
#                 configr = pdfkit.configuration(
#                     wkhtmltopdf='/app/bin/wkhtmltopdf')
#                 file = pdfkit.from_string(
#                     rendered_temp, False, css='static/css/certificate.css', configuration=configr)
#                 upload_doc(file, number=certificateno, localhost=False)
#                 download_url = f"https://cgv.s3.us-east-2.amazonaws.com/certificates/{certificateno}.pdf"
#             else:
#                 try:
#                     pdfkit.from_string(
#                         rendered_temp, f"{certificateno}.pdf", css='static/css/certificate.css')
#                 except OSError:
#                     download_url = f"http://127.0.0.1:5000/download/{certificateno}.pdf"
#             return render_template('certificate.html', postc=postc, qr_code=img_url, posto=posto, favTitle=favTitle, site_url=site_url, ip=ip_address, download_url=download_url)
#         elif (postc == None):
#             flash("No details found. Contact your organization!", "danger")
#     return render_template('Redesign-generate.html', favTitle=favTitle, ip=ip_address, user=current_user)

@app.route("/certificate/generate", methods=['GET', 'POST'])
def certificate_generate():
    if (host == True):
        try:
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        except KeyError:
            ip_address = request.remote_addr
        except Exception:
            ip_address = ipc
    else:
        ip_address = ipc
    if (request.method == 'POST'):
        certificateno = request.form.get('certificateno')
        postc = Certificate.query.filter_by(number=certificateno).first()
        if (postc != None):
            posto = Group.query.filter_by(id=postc.group_id).first()
            postf = Fonts.query.filter_by(name=posto.font_name).first()
            qr_code = QRCode.query.filter_by(
                certificate_num=certificateno).first()
            img_url = qr_code.qr_code
            return render_template('certificate.html', postf=postf, postc=postc, qr_code=img_url, posto=posto, favTitle=favTitle, site_url=site_url, number=certificateno)
        elif (postc == None):
            flash("No details found. Contact your organization!", "danger")
    return render_template('Redesign-generate.html', favTitle=favTitle, ip=ip_address, user=current_user)


# @app.route("/certify/<string:number>", methods=['GET'])
# def certificate_generate_string(number):
#     postc = Certificate.query.filter_by(number=number).first()
#     if (postc != None):
#         style = "display: none;"
#         posto = Group.query.filter_by(id=postc.group_id).first()
#         qr_code = QRCode.query.filter_by(certificate_num=number).first()
#         img_url = qr_code.qr_code
#         rendered_temp = render_template('certificate.html', postc=postc, posto=posto,
#                                         qr_code=img_url, favTitle=favTitle, site_url=site_url, number=number, style=style, pdf=True)
#         if not app.debug:
#             configr = pdfkit.configuration(wkhtmltopdf='/app/bin/wkhtmltopdf')
#             file = pdfkit.from_string(
#                 rendered_temp, False, css='static/css/certificate.css', configuration=configr)
#             upload_doc(file, number=number, localhost=False)
#             download_url = f"https://cgv.s3.us-east-2.amazonaws.com/certificates/{number}.pdf"
#         else:
#             try:
#                 pdfkit.from_string(
#                     rendered_temp, f"{number}.pdf", css='static/css/certificate.css')
#             except OSError:
#                 download_url = f"http://127.0.0.1:5000/download/{number}.pdf"
#         return render_template('certificate.html', postc=postc, posto=posto, qr_code=img_url, favTitle=favTitle, site_url=site_url, number=number, download_url=download_url, pdf=False)
#     else:
#         return redirect('/')

@app.route("/certify/<string:number>", methods=['GET'])
def certificate_generate_string(number):
    postc = Certificate.query.filter_by(number=number).first()
    if (postc != None):
        style = "display: none;"
        posto = Group.query.filter_by(id=postc.group_id).first()
        postf = Fonts.query.filter_by(name=posto.font_name).first()
        qr_code = QRCode.query.filter_by(certificate_num=number).first()
        img_url = qr_code.qr_code
        return render_template('certificate.html', postf=postf, postc=postc, posto=posto, qr_code=img_url, favTitle=favTitle, site_url=site_url, number=number, style=style)
    else:
        return redirect('/')


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    docs = os.path.join(current_app.root_path)
    return send_from_directory(directory=docs, filename=filename)


# Payment Views
@app.route("/pay", methods=["GET", "POST"])
def pay_now():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    plan = request.form.get("plan")
    plan_info = {
        "Basic Plan": 100,
        "Regular Plan": 200,
        "Premium Plan": 300
    }
    order_amount = plan_info[plan] * 100
    order_currency = 'INR'
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    order = client.order.create(
        {'amount': order_amount, 'currency': order_currency, 'payment_capture': '1'})
    context = {
        "payment": order,
        "name": name,
        "phone": phone,
        "email": email,
        "rzp_id": RAZORPAY_KEY_ID,
        "currency": order_currency
    }
    return render_template("razorpay.html", context=context)


@app.route("/razorpay-handler/", methods=["GET", "POST"])
def razorpay_handler():
    # from front end
    payment_id = request.form.get('payment_id')
    order_id = request.form.get('order_id')
    sign = request.form.get('sign')
    server_order = request.form.get('server_order')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    amount = int(request.form.get('amount')) // 100
    currency = request.form.get('currency')
    # genrate signature
    secret_key = bytes(RAZORPAY_KEY_SECRET, 'utf-8')
    generated_signature = hmac.new(secret_key, bytes(server_order + "|" + payment_id, 'utf-8'),
                                   hashlib.sha256).hexdigest()
    # checking authentic source
    if generated_signature == sign:
        new_txn = Transactions(name=name, email=email, phone=phone, order_id=order_id, amount=amount, currency=currency,
                               payment_id=payment_id, response_msg=sign, status="SUCCESS")
        db.session.add(new_txn)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/payment-failure/", methods=["GET", "POST"])
def failed_payment():
    # from front end
    payment_id = request.form.get('payment_id')
    order_id = request.form.get('order_id')
    server_order = request.form.get('server_order')
    reason = request.form.get('reason')
    step = request.form.get('step')
    source = request.form.get('source')
    description = request.form.get('description')
    code = request.form.get('code')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    amount = int(request.form.get('amount')) // 100
    currency = request.form.get('currency')
    new_txn = Transactions(name=name, email=email, phone=phone, order_id=order_id, amount=amount, currency=currency,
                           payment_id=payment_id, error_source=source, error_code=code,
                           response_msg="Step : " + step + ", Reason : " + reason + ", Desc: " + description,
                           status="FAILURE")
    db.session.add(new_txn)
    db.session.commit()
    return jsonify(success=True)


@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    # TODO: Check for active session
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        response = Users.query.filter_by(email=email).first()
        if ((response != None) and (response.status == 1) and (response.email == email) and (
                sha256_crypt.verify(password, response.password) == 1) and (response.status == 1)):
            updateloginTime = Users.query.filter_by(email=email).first()
            updateloginTime.last_login = time
            db.session.commit()
            login_user(response, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard_page'))
        else:
            flash("Invalid credentials or account not activated!", "danger")
            return render_template('login.html', favTitle=favTitle)
    else:
        return render_template('login.html', favTitle=favTitle)


@app.route('/validate/email', methods=['POST'])
def email_validation():
    data = json_lib.loads(request.data)
    email = data['email']
    pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    user = Users.query.filter_by(email=email).first()

    if user and user.status == 0:
        return jsonify(account_inactive=True)
    if user:
        return jsonify(email_error='You are already registered. Please login to continue.', status=409)
    if not bool(re.match(pattern, email)):
        return jsonify(email_pattern_error='Please enter a valid email address.')
    return jsonify(email_valid=True)


@app.route('/validate/password', methods=['POST'])
def validate_password():
    data = json_lib.loads(request.data)
    password = data["password"]
    pattern = '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[$#@!%^&*()])(?=\S+$).{8,30}$'
    if bool(re.match(pattern, password)):
        return jsonify(password_valid=True)
    return jsonify(
        password_error='Password must be 8-30 characters long and must contain atleast one uppercase letter, one lowercase letter, one number(0-9) and one special character(@,#,$,%,&,_)')


@app.route('/match/passwords', methods=["POST"])
def match_passwords():
    data = json_lib.loads(request.data)
    password1 = data['password']
    password2 = data['password2']
    if str(password1) == str(password2):
        return jsonify(password_match=True)
    return jsonify(password_mismatch='Password and Confirm Password do not match.')


def send_activation_email(name, email):
    token = s.dumps(email, salt='cgv-email-confirm')
    new_token = Token(email=email, token_id=token, status='A')
    db.session.add(new_token)
    db.session.commit()
    if app.debug:
        link = f"http://127.0.0.1:5000/confirm-email/{token}"
    else:
        link = f"{config('site_url')}/confirm-email/{token}"
    print(link)
    subject = "Welcome aboard " + name + "!"
    return send_email_now(email, subject, 'register-bot@cgv.in.net', 'Register Bot CGV', 'emails/account-activation.html', name=name, link=link)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password = sha256_crypt.hash(password)
        profile_image = avatar(email, 128)
        entry = Users(name=name, email=email, password=password, profile_image=profile_image,
                      status=0, is_staff=0, last_login=time,)
        db.session.add(entry)
        db.session.commit()
        if send_activation_email(name, email):
            flash(
                f"We've sent an account activation link on {email}", "success")
        else:
            flash("Error while sending account activation email!", "danger")
            return render_template('resend.html', favTitle=favTitle)
    return render_template('register.html', favTitle=favTitle)


@app.route('/resend-link/', methods=['GET', 'POST'])
def resend_email():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.status == 1:
                flash('Your account is already activated. Please login', 'danger')
                return redirect(url_for('resend_email'))
            name = user.name
            if send_activation_email(name, email):
                flash(
                    f"We've sent an account activation link on {email}", "success")
            else:
                flash("Error while sending account activation email!", "danger")
        else:
            flash('You are not registered yet.', 'danger')
            return redirect(url_for('resend_email'))
    return render_template("resend.html", favTitle=favTitle)


@app.route('/confirm-email/<token>', methods=['GET'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    try:
        email = s.loads(token, salt="cgv-email-confirm", max_age=1800)
    except SignatureExpired:
        db_token = Token.query.filter_by(token_id=token).first()
        db_token.status = 'E'
        flash("Sorry, link has been expired.")
        return render_template('login.html', favTitle=favTitle)
    db_token = Token.query.filter_by(token_id=token).first()
    if db_token.status == 'U':
        flash("Sorry, link has been already used.", "danger")
        return render_template("resend.html", favTitle=favTitle)
    elif db_token.status == 'E':
        flash("Sorry, link has been expired.", "danger")
        return render_template("resend.html", favTitle=favTitle)
    user = Users.query.filter_by(email=email).first()
    user.status = 1
    db_token = Token.query.filter_by(token_id=token).first()
    db_token.status = 'U'
    user.last_login = time
    db.session.commit()
    # Some error here
    if (host == True):
        try:
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        except KeyError:
            ip_address = request.remote_addr
        except Exception:
            ip_address = ipc
    else:
        ip_address = ipc
    try:
        url = requests.get("http://ip-api.com/json/{}".format(ip_address))
        j = url.json()
        city = j["city"]
        country = j["country"]
        subject = " New device login from " + \
            str(city) + ", " + str(country) + " detected."
        email_sent = send_email_now(email, subject, 'login-alert@cgv.in.net',
                                    'Security Bot CGV', 'emails/login-alert.html', city=city, country=country, time=str(time), ip_address=str(ip_address))
    except Exception:
        pass
    login_user(user)
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('dashboard_page'))


@app.route('/dashboard')
@login_required
def dashboard_page():
    postc = len(Certificate.query.order_by(Certificate.id).all())
    postct = len(Contact.query.order_by(Contact.id).all())
    postf = len(Feedback.query.order_by(Feedback.id).all())
    postn = len(Newsletter.query.order_by(Newsletter.id).all())
    return render_template('dashboard.html', favTitle=favTitle, postc=postc, postct=postct, postf=postf, postn=postn, user=current_user)


@app.route("/view/groups", methods=['GET', 'POST'])
@login_required
def view_org_page():
    if current_user.is_staff:
        post = Group.query.order_by(Group.id).all()
    else:
        post = Group.query.filter_by(
            user_id=current_user.id).order_by(Group.id).all()
    return render_template('org_table.html', post=post, favTitle=favTitle, user=current_user)


@app.route("/view/users", methods=['GET', 'POST'])
@login_required
@admin_required
def view_users_page():
    post = Users.query.order_by(Users.id).all()
    return render_template('users_table.html', post=post, favTitle=favTitle, user=current_user)


@app.route("/view/<string:grp_id>/certificates", methods=['GET', 'POST'])
@login_required
def view_certificate_page(grp_id):
    if current_user.is_staff:
        post = Certificate.query.filter_by(
            group_id=grp_id).order_by(Certificate.id)
    else:
        post = Certificate.query.filter_by(
            group_id=grp_id).order_by(Certificate.id)
    return render_template('certificate_table.html', post=post, favTitle=favTitle, c_user_name=current_user.name, user=current_user, grp_id=grp_id)


@app.route("/view/contacts", methods=['GET', 'POST'])
@login_required
@admin_required
def view_contacts_page():
    post = Contact.query.order_by(Contact.id).all()
    return render_template('contact_table.html', post=post, favTitle=favTitle, c_user_name=current_user.name, user=current_user)


@app.route("/view/feedbacks", methods=['GET', 'POST'])
@login_required
@admin_required
def view_feedbacks_page():
    post = Feedback.query.order_by(Feedback.id).all()
    return render_template('feedback_table.html', post=post, favTitle=favTitle, c_user_name=current_user.name, user=current_user)


@app.route("/view/newsletters", methods=['GET', 'POST'])
@login_required
@admin_required
def view_newsletters_page():
    post = Newsletter.query.order_by(Newsletter.id).all()
    return render_template('newsletter_table.html', post=post, favTitle=favTitle, c_user_name=current_user.name, user=current_user)


@app.route("/view/transactions", methods=['GET'])
@login_required
@admin_required
def view_transactions_page():
    post = Transactions.query.order_by(Transactions.id).all()
    return render_template('transaction_table.html', post=post, favTitle=favTitle, c_user_name=current_user.name, user=current_user)


@app.route("/view/messages/<string:id>", methods=['GET'])
@login_required
@admin_required
def view_message_page(id):
    post = Contact.query.filter_by(id=id).first()
    return render_template('view_message.html', post=post, favTitle=favTitle, c_user_name=current_user.name, user=current_user)


@app.route("/edit/<string:grp_id>/certificates/<string:id>", methods=['GET', 'POST'])
@login_required
def edit_certificates_page(grp_id, id):
    if request.method == 'POST':
        data = json_lib.loads(request.data)
        name = data["name"]
        coursename = data["course"]
        email = data["email"]
        group = Group.query.filter_by(id=grp_id).first()
        try:
            last_certificate = Certificate.query.filter_by(
                group_id=grp_id).order_by(-Certificate.id).first()
            last_certificate_num = int(
                last_certificate.number[len(last_certificate.number)-4:])
            cert_number = str(last_certificate_num + 1).zfill(4)
        except Exception as e:
            cert_number = '1'.zfill(4)
        number = group.prefix + cert_number
        userid = current_user.id
        last_update = x
        if id == '0':
            postcheck = Certificate.query.filter_by(
                email=email, group_id=grp_id).first()
            if (postcheck == None):
                try:
                    post = Certificate(name=name, number=number, email=email, coursename=coursename, user_id=userid, is_email_sent=False,
                                       group_id=grp_id, last_update=last_update)
                    db.session.add(post)
                    db.session.commit()
                    # Create QR Code for this certificate
                    link = f'{config("site_url")}/certify/{number}'
                    new_qr = QRCode(certificate_num=number, link=link)
                    qr_image = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr_image.add_data(link)
                    qr_image.make(fit=True)
                    img = qr_image.make_image(fill='black', back_color='white')
                    buffer = io.BytesIO()
                    img.save(buffer, format="PNG")
                    buffer.seek(0)
                    try:
                        if not app.debug:
                            # upload_image(buffer, number=number,
                            #              folder="qr_codes")
                            # img_url = f"https://cgv.s3.us-east-2.amazonaws.com/qr_codes/{number}.png"
                            img_url = upload(buffer)
                        else:
                            try:
                                os.mkdir("static/qr_codes")
                            except Exception:
                                pass
                            img.save("static/qr_codes/"+f"{number}.png")
                            img_url = f"http://127.0.0.1:5000/static/qr_codes/{number}.png"
                        new_qr.qr_code = f"{img_url}"
                        new_qr.certificate_id = post.id
                        db.session.add(new_qr)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                    subject = f"Certificate Generated With Certificate Number : {number}"
                    email_sent = send_email_now(email, subject, 'certificate-bot@cgv.in.net', 'Certificate Generate Bot CGV',
                                                'emails/new-certificate.html', number=str(number), name=name, site_url=config("site_url"))
                    if not email_sent:
                        flash("Error while sending mail!", "danger")
                    else:
                        post.is_email_sent = True
                        db.session.add(post)
                        db.session.commit()
                        flash(
                            "An email with certificate details has been sent!", "success")
                    return jsonify(certificate_success=True)
                except Exception as e:
                    print(e)
                    return jsonify(certificate_error=True)
            else:
                return jsonify(certificate_duplicate=True)
        else:
            try:
                post = Certificate.query.filter_by(id=id).first()
                post.name = name
                post.coursename = coursename
                post.email = email
                post.user_id = current_user.id
                post.group_id = grp_id
                post.last_update = time
                db.session.commit()
                return jsonify(certificate_success=True)
            except Exception as e:
                print(e)
                return jsonify(certificate_error=True)
    cert = Certificate.query.filter_by(id=id).first()
    post = {
        "id": cert.id,
        "name": cert.name,
        "coursename": cert.coursename,
        "email": cert.email,
        "last_update": cert.last_update,
        "number": cert.number
    }
    return jsonify(favTitle=favTitle, id=id, post=post)


@app.get('/send-email/<string:grp_id>')
@login_required
def send_group_email(grp_id):
    all_certificates = Certificate.query.filter_by(group_id=grp_id).all()
    for cert in all_certificates:
        if not cert.is_email_sent:
            subject = "Certificate Generated With Certificate Number : " + \
                str(cert.number)
            try:
                send_email_now(cert.email, subject, 'certificate-bot@cgv.in.net', 'Certificate Generate Bot CGV',
                               'emails/new-certificate.html', number=cert.number, name=cert.name, site_url=config("site_url"))
                cert.is_email_sent = True
                db.session.add(cert)
                db.session.commit()
            except Exception:
                pass
    return redirect(f"/view/{grp_id}/certificates")


@app.route('/upload/<string:grp_id>/certificate', methods=['POST', 'GET'])
@login_required
def upload_csv(grp_id):
    group = Group.query.filter_by(id=grp_id).first()
    csv_file = request.files['fileToUpload']
    csv_file = io.TextIOWrapper(csv_file, encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter=',')
    # This skips the first row of the CSV file.
    next(csv_reader)
    for row in csv_reader:
        try:
            last_certificate = Certificate.query.filter_by(
                group_id=grp_id).order_by(-Certificate.id).first()
            last_certificate_num = int(
                last_certificate.number[len(last_certificate.number)-4:])
            cert_number = str(last_certificate_num + 1).zfill(4)
        except Exception as e:
            cert_number = '1'.zfill(4)
        number = group.prefix + cert_number
        certificate = Certificate(
            number=number, name=row[0], email=row[1], coursename=row[2], user_id=current_user.id, group_id=grp_id, is_email_sent=False, last_update=time)
        db.session.add(certificate)
        db.session.commit()
        # Create QR Code for this certificate
        link = f'{config("site_url")}/certify/{number}'
        new_qr = QRCode(certificate_num=number, link=link)
        qr_image = qrcode.QRCode(version=1, box_size=10, border=5)
        qr_image.add_data(link)
        qr_image.make(fit=True)
        img = qr_image.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        try:
            if not app.debug:
                # upload_image(buffer, number=number, folder="qr_codes")
                # img_url = f"https://cgv.s3.us-east-2.amazonaws.com/qr_codes/{number}.png"
                img_url = upload(buffer)
            else:
                try:
                    os.mkdir("static/qr_codes")
                except Exception:
                    pass
                img.save("static/qr_codes/"+f"{number}.png")
                img_url = f"http://127.0.0.1:5000/static/qr_codes/{number}.png"
            new_qr.qr_code = f"{img_url}"
            new_qr.certificate_id = certificate.id
            db.session.add(new_qr)
            db.session.commit()

        except Exception as e:
            print(e)
    return jsonify(result=True, status=200)

# For Certificate


def row_to_list(obj):
    lst = []
    lst.append(obj.number)
    lst.append(obj.name)
    lst.append(obj.email)
    lst.append(obj.coursename)
    lst.append(obj.last_update)
    return lst


@app.route("/download/<string:grp_id>/certificate")
def export_certificate_csv(grp_id):
    all_certificates = Certificate.query.filter_by(
        group_id=grp_id).order_by(Certificate.id)
    if all_certificates.count() <= 0:
        flash("No certificates available in this group", "danger")
        return redirect(f"/view/{grp_id}/certificates")
    si = io.StringIO()
    cw = csv.writer(si, delimiter=",")
    cw.writerow(["Number", "Name", "Email", "Course Name", "Date Created"])
    for row in all_certificates:
        row = row_to_list(row)
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=group{grp_id}.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route("/activate/user/<string:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def activate_users(id):
    activate = Users.query.filter_by(id=id).first()
    if (activate.email == config("admin_email")):
        flash("Administrator account will always be active!", "warning")
        return redirect(url_for('view_users_page'))
    else:
        if (activate.status == 1):
            activate.status = 0
            flash("User account deactivated!", "warning")
            db.session.commit()
            return redirect(url_for('view_users_page'))
        else:
            activate.status = 1
            flash("User account activated!", "success")
            db.session.commit()
            return redirect(url_for('view_users_page'))


@app.route("/permissions/<string:perm>/users/<string:id>", methods=['GET', 'POST'])
@login_required
def change_permissions(perm, id):
    user = Users.query.filter_by(id=id).first()
    if current_user.is_admin:
        if current_user.id != user.id:
            if perm == 'staff':
                if user.is_staff:
                    user.is_staff = False
                else:
                    user.is_staff = True
            elif perm == 'admin':
                if user.is_admin:
                    user.is_admin = False
                else:
                    user.is_admin = True
            db.session.commit()
        else:
            flash("You cannot change your own permission", "danger")
    else:
        flash("You are not authorised to change permissions", "danger")
    return redirect(url_for('view_users_page'))


@app.route('/get-all-groups', methods=['GET'])
@login_required
def get_all_groups():
    groups = Group.query.filter_by(user_id=current_user.id).all()
    data = {'group': [[group.id, group.name] for group in groups]}
    return jsonify(data)


@app.route("/edit/group/<string:id>", methods=['GET', 'POST'])
@login_required
def edit_org_page(id):
    if request.method == 'POST':
        name = request.form.get("name")
        certx = request.form.get("certx")
        certy = request.form.get("certy")
        qrx = request.form.get("qrx")
        qry = request.form.get("qry")
        certnox = request.form.get("certnox")
        certnoy = request.form.get("certnoy")
        font_size = request.form.get("font_size")
        font_name = request.form.get("font_name")
        textColor = request.form.get("textColor")
        bg_image = request.files.get("bg_image")
        prefix = request.form.get("prefix")
        date = x
        if id == '0':
            if Group.query.filter_by(name=name, user_id=current_user.id).first():
                return jsonify(group_duplicate=True)
            try:
                post = Group(name=name, textColor=textColor, font_size=font_size, font_name=font_name,  certx=certx, certy=certy, qrx=qrx, qry=qry,
                             certnox=certnox, certnoy=certnoy, prefix=prefix, date=date, user_id=current_user.id)
                img_name = name.replace(" ", "+")
                if not app.debug:
                    # upload_image(bg_image, folder="backgrounds", name=name)
                    # bg_url = f"https://cgv.s3.us-east-2.amazonaws.com/backgrounds/{img_name}.png"
                    bg_url = upload(bg_image)
                else:
                    try:
                        os.mkdir("static/backgrounds")
                    except Exception:
                        pass
                    bg_image.save(f"static/backgrounds/{img_name}.png")
                    bg_url = f"http://127.0.0.1:5000/static/backgrounds/{img_name}.png"
                post.bg_image = bg_url
                db.session.add(post)
                db.session.commit()
                db.session.commit()
                return jsonify(result=True, status=200)
            except Exception:
                return jsonify(group_error=True)
        else:
            try:
                post = Group.query.filter_by(id=id).first()
                post.name = name
                img_name = name.replace(" ", "+")
                if bg_image:
                    if not app.debug:
                        # upload_image(bg_image, folder="backgrounds", name=name)
                        # bg_url = f"https://cgv.s3.us-east-2.amazonaws.com/backgrounds/{img_name}.png"
                        bg_url = upload(bg_image)
                    else:
                        bg_image.save(f"static/backgrounds/{name}")
                        bg_url = f"http://127.0.0.1:5000/static/backgrounds/{name}"
                post.bg_image = bg_url
                post.date = date
                post.certx = certx
                post.certy = certy
                post.qrx = qrx
                post.qry = qry
                post.font_name = font_name
                post.font_size = font_size
                post.certnox = certnox
                post.certnoy = certnoy
                post.textColor = textColor
                post.user_id = current_user.id
                db.session.commit()
                return jsonify(result=True, status=200)
            except Exception:
                return jsonify(result=False, status=500)
    grp = Group.query.filter_by(id=id).first()
    post = {
        "id": grp.id,
        "name": grp.name,
        "certx": grp.certx,
        "certy": grp.certy,
        "qrx": grp.qrx,
        "qry": grp.qry,
        "certnox": grp.certnox,
        "certnoy": grp.certnoy,
        "font_size": grp.font_size,
        "font_name": grp.font_name,
        "textColor": grp.textColor,
    }
    return jsonify(favTitle=favTitle, id=id, post=post)


@app.route("/delete/group/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_org_page(id):
    delete_org_page = Group.query.filter_by(id=id).first()
    try:
        db.session.delete(delete_org_page)
        db.session.commit()
        # delete_from_s3(file=f'signatures/{delete_org_page.name}')
        # delete_from_s3(file=f'backgrounds/{delete_org_page.name}')
        flash("Group deleted successfully!", "success")
    except Exception:
        flash("Something went wrong!", "error")
    return redirect('/view/groups')


@app.route("/delete/users/<string:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def delete_users_page(id):
    delete_users_page = Users.query.filter_by(id=id).first()
    if (delete_users_page.email == config("admin_email")) or delete_users_page.is_staff:
        flash("You can't delete administrator!", "danger")
    else:
        db.session.delete(delete_users_page)
        db.session.commit()
        flash("User deleted successfully!", "success")
        return redirect('/view/users')
    return redirect('/view/users')


@app.route("/delete/<string:grp_id>/certificates/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_certificates_page(grp_id, id):
    delete_certificates_page = Certificate.query.filter_by(id=id).first()
    db.session.delete(delete_certificates_page)
    db.session.commit()
    flash("Certificate deleted successfully!", "success")
    return redirect(f'/view/{grp_id}/certificates')


@app.route("/delete/contact/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_contact_page(id):
    delete_contact_page = Contact.query.filter_by(id=id).first()
    db.session.delete(delete_contact_page)
    db.session.commit()
    flash("Contact response deleted successfully!", "success")
    return redirect('/view/contacts')


@app.route("/delete/feedback/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_feedback_page(id):
    delete_feedback_page = Feedback.query.filter_by(id=id).first()
    db.session.delete(delete_feedback_page)
    db.session.commit()
    flash("Feedback response deleted successfully!", "success")
    return redirect('/view/feedbacks')


@app.route("/delete/newsletter/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_newsletter_page(id):
    delete_newsletter_page = Newsletter.query.filter_by(id=id).first()
    db.session.delete(delete_newsletter_page)
    db.session.commit()
    flash("Newsletter response deleted successfully!", "success")
    return redirect('/view/newsletters')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully!', 'success')
    return redirect(url_for('loginPage'))


# Google Login Starts Here

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Google Login Route


@app.route('/login/google')
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let us retrieve user's profile from Google

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route('/login/google/callback')
def google_login_callback():
    # Get authorization code Google sent back to us
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow us to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json_lib.dumps(token_response.json()))

    # Now that we have tokens, let's find and hit the URL
    # from Google that gives us the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["name"]
    else:
        abort(401)
    # Create a user in your db with the information provided
    # by Google

    # Doesn't exist? Add it to the database.
    if not Users.query.filter_by(email=users_email).first():
        pwo = PasswordGenerator()
        pwd = pwo.generate()
        password = sha256_crypt.hash(pwd)
        entry = Users(name=users_name, email=users_email, password=password,
                      profile_image=picture, last_login=time, status=1, is_staff=False)
        db.session.add(entry)
        db.session.commit()

    # Begin user session by logging the user in

    user = Users.query.filter_by(email=users_email).first()
    if user.status == 1:
        login_user(user)
    else:
        flash("Your account has been deactivated. Contact us to activate it.", "danger")
        return redirect(url_for("loginPage"))

    # Send user back to homepage
    return redirect(url_for("dashboard_page"))


# FB_SCOPE = ["email", "public_profile"]


# @app.route('/login/facebook')
# def facebook_login():
#     facebook = requests_oauthlib.OAuth2Session(
#         FB_CLIENT_ID, redirect_uri=request.base_url + "/fb-callback", scope=FB_SCOPE
#     )
#     authorization_url, _ = facebook.authorization_url(
#         FB_AUTHORIZATION_BASE_URL)

#     return redirect(authorization_url)


# @app.route('/login/facebook/callback')
# def facebook_login_callback():
#     facebook = requests_oauthlib.OAuth2Session(
#         FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=request.base_url + "/callback"
#     )

#     # we need to apply a fix for Facebook here
#     facebook = facebook_compliance_fix(facebook)

#     facebook.fetch_token(
#         FB_TOKEN_URL,
#         client_secret=FB_CLIENT_SECRET,
#         authorization_response=request.url,
#     )

#     # Fetch a protected resource, i.e. user profile, via Graph API

#     facebook_user_data = facebook.get(
#         "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
#     ).json()

#     users_email = facebook_user_data["email"]
#     users_name = facebook_user_data["name"]
#     picture_url = facebook_user_data.get(
#         "picture", {}).get("data", {}).get("url")

#     pwo = PasswordGenerator()
#     pwd = pwo.generate()
#     password = sha256_crypt.hash(pwd)
#     if not Users.query.filter_by(email=users_email).first():
#         entry = Users(name=users_name, email=users_email, password=password,
#                       profile_image=picture_url, last_login=time, status=1)
#         db.session.add(entry)
#         db.session.commit()

#     user = Users.query.filter_by(email=users_email).first()
#     login_user(user)

#     # Send user back to homepage
#     return redirect(url_for("dashboard_page"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def user_not_authorized(e):
    return render_template('401.html'), 401

# for feedback


def rowToListFeedback(obj):
    lst = []
    name = obj.name
    email = obj.email
    rating = obj.rating
    msg = obj.message
    lst.append(name)
    lst.append(email)
    lst.append(rating)
    lst.append(msg)
    return lst


@app.route('/downloadfeedback')
@login_required
@admin_required
def ToCsv():
    allfeedback = Feedback.query.all()
    if len(allfeedback) == 0:
        flash("No Feedback available", "danger")
        return redirect("/view/feedbacks")
    si = io.StringIO()
    cw = csv.writer(si, delimiter=",")
    cw.writerow(["Name",  "Email", "Rating Out of 5", "Message"])
    for row in allfeedback:
        row = rowToListFeedback(row)
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=feedback_response.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# for contact


def rowToListContact(obj):
    lst = []
    name = obj.name
    email = obj.email
    number = obj.phone
    msg = obj.message[3:-4]
    date = obj.date
    ip = obj.ip
    lst.append(name)
    lst.append(email)
    lst.append(number)
    lst.append(msg)
    lst.append(date)
    lst.append(ip)
    return lst


@app.route('/downloadcontact')
@login_required
@admin_required
def ContactToCsv():
    allfeedback = Contact.query.all()
    if len(allfeedback) == 0:
        flash("No Contacts available", "danger")
        return redirect("/view/contacts")
    si = io.StringIO()
    cw = csv.writer(si, delimiter=",")
    cw.writerow(["Name", "Email", "Number", "Message", "Date", "IP"])
    for row in allfeedback:
        row = rowToListContact(row)
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=contact_response.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# for Newsletter
def rowToListNewsletter(obj):
    lst = []
    email = obj.email
    ip = obj.ip
    date = obj.date
    lst.append(email)
    lst.append(ip)
    lst.append(date)
    return lst


@app.route('/downloadNewsletter')
@login_required
@admin_required
def NewsletterToCsv():
    allfeedback = Newsletter.query.all()
    if len(allfeedback) == 0:
        flash("No Newsletter available", "danger")
        return redirect("/view/newsletters")
    si = io.StringIO()
    cw = csv.writer(si, delimiter=",")
    cw.writerow(["Email", "IP", "Date"])
    for row in allfeedback:
        row = rowToListNewsletter(row)
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=NewsLetter.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# API PART STARTS HERE


@app.route('/api-keys/view/private', methods=['GET'])
@login_required
def view_all_private_api_keys():
    if current_user.is_staff:
        postc = APIKey.query.order_by(APIKey.id).all()
        return render_template('private_api_admin_table.html', user=current_user, favTitle=favTitle, postc=postc)
    groups = Group.query.filter_by(user_id=current_user.id).all()
    postc = []
    for grp in groups:
        data = APIKey.query.filter_by(group_id=grp.id).first()
        if data:
            postc.append(data)
    return render_template('private_api_users_table.html', user=current_user, favTitle=favTitle, postc=postc)


@app.route('/api-keys/view/public', methods=['GET'])
@login_required
def view_all_public_api_keys():
    if current_user.is_staff:
        postc = PublicAPIKey.query.order_by(PublicAPIKey.id).all()
        return render_template('public_api_admin_table.html', user=current_user, favTitle=favTitle, postc=postc)
    postc = PublicAPIKey.query.filter_by(email=current_user.email).all()
    return render_template('public_api_users_table.html', user=current_user, favTitle=favTitle, postc=postc)


def create_random_api():
    data = list(string.ascii_uppercase) + \
        list(string.ascii_lowercase) + list(string.digits) + \
        ['@', '#', '$', '%', '&', '_']
    key = ''.join(random.choice(data) for _ in range(20))
    api_key = 'CGV.'+key
    return api_key


@app.route('/api-key/generate/<int:grp_id>', methods=['POST'])
@login_required
def generate_api_key(grp_id):
    if APIKey.query.filter_by(group_id=grp_id).first():

        return jsonify(key_error="You've already generated an API Key for this organization.")
    try:
        group_name = Group.query.filter_by(id=grp_id).first().name
        new_api = APIKey(key=create_random_api(), user_id=current_user.id,
                         group_id=grp_id, group_name=group_name, usage_limit=0, date_generated=x)
        db.session.add(new_api)
        db.session.commit()
        return jsonify(key_success='API Key has been generated successfully. within 8 hours.')
    except Exception as e:
        print(e)
        return jsonify(key_error='Something went wrong while generating API Key for you.')


@app.route('/api-key/generate/public-api', methods=['GET'])
@login_required
def generate_pub_api_key():
    if PublicAPIKey.query.filter_by(email=current_user.email).first():
        flash("You've already generated a Public API Key for this account.", 'danger')
    try:
        new_api = PublicAPIKey(key=create_random_api(),
                               email=current_user.email, date_generated=x)
        db.session.add(new_api)
        db.session.commit()
        flash('Public API Key has been generated successfully. An admin should approve it within 8 hours.', 'success')

    except Exception as e:
        print(e)
        flash('Something went wrong while generating API Key for you.', 'danger')
    return redirect(url_for('view_all_public_api_keys'))


@app.route('/api-key/private/approve/<int:grp_id>', methods=['GET', 'POST'])
def approve_private_api_key(grp_id):
    try:
        api_key = APIKey.query.filter_by(group_id=grp_id).first()
        data = json_lib.loads(request.data)
        api_key.usage_limit = data['usage_limit']
        api_key.is_approved, api_key.is_valid = True, True
        db.session.add(api_key)
        db.session.commit()
        return jsonify(key_approved='API Key has been approved successfully!')
    except Exception:
        return jsonify(key_error='Something went wrong while approving the API Key!')


@app.route('/api-key/public/approve/<int:api_id>', methods=['GET'])
def approve_public_api_key(api_id):
    try:
        api_key = PublicAPIKey.query.filter_by(id=api_id).first()
        api_key.is_approved, api_key.is_valid = True, True
        db.session.add(api_key)
        db.session.commit()
        return jsonify(key_approved='API Key has been approved successfully!')
    except Exception:
        return jsonify(key_error='Something went wrong while approving the API Key!')


@app.route('/v1/api/certificates', methods=['GET'])
def get_groups_data():
    # Here we'll have an argument like ?group=1
    header_api_key = request.headers.get(
        'X-API-KEY') or request.headers.get('x-api-key')
    # If api key is not passed in request header
    if not header_api_key:
        data = {
            'status': 401,
            'message': "You're not authorized to access the resource. Please add X-API-KEY in request header."
        }
        return jsonify(data), 401
    group_id = request.args.get('group')
    # If group id is not passed in request url
    if not group_id:
        data = {
            'status': '406',
            'message': "Welcome to CGV API V1. There is no content to send for this request, please add argument like ?group=id in the request url"
        }
        return jsonify(data), 406
    api_key = APIKey.query.filter_by(key=header_api_key).first()
    # Check if api key exists and is valid
    if api_key and api_key.is_valid and api_key.group_id == group_id:
        certificates = Certificate.query.filter_by(group_id=group_id).all()
        # Check if certificate exists with the mentioned group id
        if certificates:
            response_data = []
            for cert in certificates:
                data = {
                    'user_name': cert.name,
                    'course_name': cert.coursename,
                    'group_name': api_key.group_name,
                    'cert_number': cert.number,
                    'cert_link': f'https://cgv.in.net/certify/{cert.number}',
                    'date_generated': cert.last_update[:10]
                }
                response_data.append(data)
                # Decrease the limit by 1 and if it becomes 0, make the api key invalid
            api_key.usage_limit -= 1
            if api_key.usage_limit == 0:
                api_key.is_valid = False
            db.session.add(api_key)
            db.session.commit()
            # Success Response
            return jsonify(response_data), 200
        # If no certificates with the group id
        data = {
            'status': 404,
            'message': 'We either could not find the group or there is no certificate in the group'
        }
        # Decrease the limit by 1 and if it becomes 0, make the api key invalid
        api_key.usage_limit -= 1
        if api_key.usage_limit == 0:
            api_key.is_valid = False
        db.session.add(api_key)
        db.session.commit()
        return jsonify(data), 404
    # Invalid API Key
    data = {
        'status': 403,
        'message': "Please add a valid API Key in the request header."
    }
    return jsonify(data), 403


@app.route('/v1/api/certificates/all', methods=['GET'])
def get_all_certificates():
    header_api_key = request.headers.get(
        'X-API-KEY') or request.headers.get('x-api-key')
    if not header_api_key:
        data = {
            'status': 401,
            'message': "You're not authorised to access the resource. Please add X-API-KEY in request header."
        }
        return jsonify(data), 401
    api_key = PublicAPIKey.query.filter_by(key=header_api_key).first()
    if api_key and api_key.is_valid:
        user_id = Users.query.filter_by(email=api_key.email).first().id
        groups = Group.query.filter_by(user_id=user_id).all()
        response_data = []
        for grp in groups:
            grp_data = []
            certificates = Certificate.query.filter_by(group_id=grp.id).all()
            for cert in certificates:
                data = {
                    'user_name': cert.name,
                    'course_name': cert.coursename,
                    'group_name': Group.query.filter_by(id=cert.group_id).first().name,
                    'cert_number': cert.number,
                    'cert_link': f'https://cgv.in.net/certify/{cert.number}',
                    'date_generated': cert.last_update[:10]
                }
                grp_data.append(data)
            response_data.append({grp.name: grp_data})
        return jsonify(response_data), 200

    # Invalid API Key
    data = {
        'status': 403,
        'message': "Please add a valid API Key in the request header."
    }
    return jsonify(data), 403


@app.post('/v1/api/certificates')
def post_new_certificate():
    # Here we'll have an argument like ?group=1
    header_api_key = request.headers.get(
        'X-API-KEY') or request.headers.get('x-api-key')
    # If api key is not passed in request header
    if not header_api_key:
        data = {
            'status': 401,
            'message': "You're not authorised to access the resource. Please add X-API-KEY in request header."
        }
        return jsonify(data), 401
    group_id = request.args.get('group')
    # If group id is not passed in request url
    if not group_id:
        data = {
            'status': '406',
            'message': "Welcome to CGV API V1. There is no content to send for this request, please add argument like ?group=id in the request url"
        }
        return jsonify(data), 406
    api_key = APIKey.query.filter_by(key=header_api_key).first()
    if api_key and api_key.is_valid:
        if api_key.group_id == int(group_id):
            data = request.json
            if data:
                if not data.get("name"):
                    return jsonify({'status': 400, 'message': "Please enter user's name"}), 400
                if not data.get("email"):
                    return jsonify({'status': 400, 'message': "Please enter user's email"}), 400
                if not data.get("course"):
                    return jsonify({'status': 400, 'message': 'Please enter course'}), 400
            else:
                return jsonify({'status': 400, 'message': 'Empty Body'}), 400
            name = data["name"]
            course = data["course"]
            email = data["email"]
            postcheck = Certificate.query.filter_by(
                email=email, group_id=group_id).first()
            if not postcheck:
                group = Group.query.filter_by(id=group_id).first()
                try:
                    last_certificate = Certificate.query.filter_by(
                        group_id=group_id).order_by(-Certificate.id).first()
                    last_certificate_num = int(
                        last_certificate.number[len(last_certificate.number)-4:])
                    cert_number = str(last_certificate_num + 1).zfill(4)
                except Exception:
                    cert_number = '1'.zfill(4)
                number = group.prefix + cert_number
                try:
                    new_cert = Certificate(name=name, number=number, email=email, coursename=course,
                                           user_id=api_key.user_id, is_email_sent=True, group_id=group_id, last_update=x)
                    db.session.add(new_cert)
                    db.session.commit()
                    # Create QR Code for this certificate
                    link = f'{config("site_url")}/certify/{number}'
                    new_qr = QRCode(certificate_num=number, link=link)
                    qr_image = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr_image.add_data(link)
                    qr_image.make(fit=True)
                    img = qr_image.make_image(fill='black', back_color='white')
                    buffer = io.BytesIO()
                    img.save(buffer, format="PNG")
                    buffer.seek(0)
                    try:
                        if not app.debug:
                            img_url = upload(buffer)
                        else:
                            try:
                                os.mkdir("static/qr_codes")
                            except Exception:
                                pass
                            img.save("static/qr_codes/"+f"{number}.png")
                            img_url = f"http://127.0.0.1:5000/static/qr_codes/{number}.png"
                        new_qr.qr_code = f"{img_url}"
                        new_qr.certificate_id = new_cert.id
                        db.session.add(new_qr)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                    subject = "Certificate Generated With Certificate Number : " + \
                        str(number)
                    send_email_now(email, subject, 'certificate-bot@cgv.in.net', 'Certificate Generate Bot CGV',
                                   'emails/new-certificate.html', number=str(number), name=name, site_url=config("site_url"))
                    new_cert.is_email_ent = True
                    db.session.add(new_cert)
                    db.session.commit()
                    data = {
                        'status': '200',
                        'message': "Certificate has been generated successfully.",
                        'certificate': {
                            'user_name': new_cert.name,
                            'course_name': new_cert.coursename,
                            'group_name': api_key.group_name,
                            'cert_number': new_cert.number,
                            'cert_link': f'https://cgv.in.net/certify/{new_cert.number}',
                            'date_generated': new_cert.last_update[:10]
                        }
                    }
                    return jsonify(data), 200
                except Exception:
                    data = {
                        'status': '500',
                        'message': "Server encountered some error while generating certificate.",
                    }
                    return jsonify(data), 500
            else:
                data = {
                    'status': 409,
                    'message': "Certificate already exists"
                }
                return jsonify(data), 409
        else:
            data = {
                'status': 401,
                'message': "You're not authorised to add certificate in this group."
            }
            return jsonify(data), 409
    # Invalid API Key
    data = {
        'status': 403,
        'message': "Please add a valid API Key in the request header."
    }
    return jsonify(data), 403


@app.put('/v1/api/certificates')
def update_certificate():
    # Here we'll have an argument like ?group=1
    header_api_key = request.headers.get(
        'X-API-KEY') or request.headers.get('x-api-key')
    # If api key is not passed in request header
    if not header_api_key:
        data = {
            'status': 401,
            'message': "You're not authorised to access the resource. Please add X-API-KEY in request header."
        }
        return jsonify(data), 401
    certificate_id = request.args.get('id')
    # If group id is not passed in request url
    if not certificate_id:
        data = {
            'status': '406',
            'message': "Welcome to CGV API V1. There is no content to send for this request, please add argument like ?id=certificate-id in the request url"
        }
        return jsonify(data), 406
    api_key = APIKey.query.filter_by(key=header_api_key).first()
    if api_key and api_key.is_valid:
        certificate = Certificate.query.filter_by(id=certificate_id).first()
        if certificate:
            if api_key.group_id == certificate.group_id:
                data = request.json
                if not data:
                    return jsonify({'status': 400, 'message': 'Empty Body'}), 400
                name = data["name"] if data.get("name") else certificate.name
                course = data["course"] if data.get(
                    "course") else certificate.coursename
                email = data["email"] if data.get(
                    "email") else certificate.email
                try:
                    certificate.name = name
                    certificate.coursename = course
                    certificate.email = email
                    certificate.last_update = x
                    db.session.add(certificate)
                    db.session.commit()
                    data = {
                        'status': 200,
                        'message': 'Certificate updated successfully!',
                        'certificate': {
                            'user_name': certificate.name,
                            'course_name': certificate.coursename,
                            'group_name': api_key.group_name,
                            'cert_number': certificate.number,
                            'cert_link': f'https://cgv.in.net/certify/{certificate.number}',
                            'date_generated': certificate.last_update[:10]
                        }
                    }
                    return jsonify(data), 200
                except Exception:
                    data = {
                        'status': '500',
                        'message': "Server encountered some error while updating certificate.",
                    }
                    return jsonify(data), 500
            else:
                data = {
                    'status': 401,
                    'message': "You're not authorised to add certificate in this group."
                }
                return jsonify(data), 409
        else:
            data = {
                'status': 404,
                'message': 'No such certificate found'
            }
            return jsonify(data), 404
    # Invalid API Key
    data = {
        'status': 403,
        'message': "Please add a valid API Key in the request header."
    }
    return jsonify(data), 403


@app.delete('/v1/api/certificates')
def delete_certificate():
    # Here we'll have an argument like ?group=1
    header_api_key = request.headers.get(
        'X-API-KEY') or request.headers.get('x-api-key')
    # If api key is not passed in request header
    if not header_api_key:
        data = {
            'status': 401,
            'message': "You're not authorised to access the resource. Please add X-API-KEY in request header."
        }
        return jsonify(data), 401
    certificate_id = request.args.get('id')
    # If group id is not passed in request url
    if not certificate_id:
        data = {
            'status': '406',
            'message': "Welcome to CGV API V1. There is no content to send for this request, please add argument like ?id=certificate-id in the request url"
        }
        return jsonify(data), 406
    api_key = APIKey.query.filter_by(key=header_api_key).first()
    if api_key and api_key.is_valid:
        certificate = Certificate.query.filter_by(id=certificate_id).first()
        if certificate:
            if api_key.group_id == certificate.group_id:
                try:
                    db.session.delete(certificate)
                    db.session.commit()
                    data = {
                        'status': 200,
                        'message': 'Certificate deleted successfully!',
                    }
                    return jsonify(data), 200
                except Exception:
                    data = {
                        'status': '500',
                        'message': "Server encountered some error while deleting certificate.",
                    }
                    return jsonify(data), 500
            else:
                data = {
                    'status': 401,
                    'message': "You're not authorised to delete certificate from this group."
                }
                return jsonify(data), 409
        else:
            data = {
                'status': 404,
                'message': 'No such certificate found'
            }
            return jsonify(data), 404
    # Invalid API Key
    data = {
        'status': 403,
        'message': "Please add a valid API Key in the request header."
    }
    return jsonify(data), 403

# API PART ENDS HERE


@login_required
@app.route('/<int:id>/profile/edit', methods=['GET', 'POST'])
def profile(id):
    name = request.form.get("name")
    profile_pic = request.files.get("profile_pic")
    try:
        user = Users.query.filter_by(id=id).first()
        if name:
            user.name = name
        img_name = name.replace(" ", "+")
        if profile_pic:
            if not app.debug:
                # upload_image(profile_pic, folder="profile_pics", name=name)
                # img_url = f"https://cgv.s3.us-east-2.amazonaws.com/profile_pics/{img_name}"
                img_url = upload(profile_pic)
            else:
                try:
                    os.mkdir("static/profile_pics")
                except Exception:
                    pass
                profile_pic.save(f"static/profile_pics/{img_name}.png")
                img_url = f"http://127.0.0.1:5000/static/profile_pics/{img_name}.png"
            user.profile_image = img_url
        db.session.add(user)
        db.session.commit()
        return jsonify(result=True), 200
    except Exception as e:
        print(e)
        return jsonify(result=False), 500


@app.route('/get-all-fonts', methods=['GET'])
@login_required
def get_all_fonts():
    fonts = Fonts.query.order_by(Fonts.id).all()
    data = {'font': [fonts.name for fonts in fonts]}
    return jsonify(data)


@app.route("/view/fonts", methods=['GET', 'POST'])
@login_required
@admin_required
def view_fonts_page():
    post = Fonts.query.order_by(Fonts.id).all()
    return render_template('font_table.html', post=post, favTitle=favTitle, c_user_name=current_user.name, user=current_user)


@app.route("/add/fonts", methods=['GET', 'POST'])
@login_required
def add_font():
    if request.method == 'POST':
        name = request.form.get("name")
        font = request.form.get("font")
        entry = Fonts(name=name, font_cdn=font)
        db.session.add(entry)
        db.session.commit()
        return jsonify(result=True, status=200)


@app.route("/delete/font/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_font_page(id):
    delete_font_page = Fonts.query.filter_by(id=id).first()
    db.session.delete(delete_font_page)
    db.session.commit()
    flash("Font deleted successfully!", "success")
    return redirect('/view/fonts')


if __name__ == '__main__':
    app.run(debug=True)
