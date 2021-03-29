import os
from flask.globals import current_app
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, render_template, redirect, request, flash, url_for, jsonify, abort, send_from_directory
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from password_generator import PasswordGenerator
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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

# work done by arpit
# start

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check(email):
    return re.search(regex, email)


# end
with open('import.json', 'r') as c:
    json = json_lib.load(c)["jsondata"]

app = Flask(__name__)
app.config.from_object(json['app_settings'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# serializer for registration
s = URLSafeTimedSerializer(app.secret_key)


login_manager = LoginManager(app)
login_manager.login_view = 'loginPage'
login_manager.login_message_category = 'info'

RAZORPAY_KEY_ID = json["razorpay_key_id"]
RAZORPAY_KEY_SECRET = json["razorpay_key_secret"]

# Google Login Credentials
GOOGLE_CLIENT_ID = json["google_client_id"]
GOOGLE_CLIENT_SECRET = json["google_client_secret"]
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

IST = pytz.timezone('Asia/Kolkata')
x = datetime.now(IST)
time = x.strftime("%c")
host = bool(json["host_status"])
ipc = json["demo_ip"]


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


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    certificates = db.relationship(
        'Certificate', cascade="all,delete", backref='certificates')


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    coursename = db.Column(db.String(500), nullable=False)
    last_update = db.Column(db.String(50), nullable=False)
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


# For Gravatar
def avatar(email, size):
    digest = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


def send_password_reset_email(name, email):
    token = s.dumps(email, salt='cgv-password-reset')
    print(token)
    if app.debug:
        link = f"http://127.0.0.1:5000/reset-password/{token}"
    else:
        link = f"{json['site_url']}/reset-password/{token}"
    print(link)
    subject = "Password Reset Link | CGV"
    content1 = '''<!DOCTYPE html><html lang="en" ><head><meta charset="UTF-8"><title>Register CGV</title></head><body><table cellspacing="0" cellpadding="0" border="0" style="color:#333;background:#fff;padding:0;margin:0;width:100%;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><tbody><tr width="100%"><td valign="top" align="left" style="background:#eef0f1;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><table style="border:none;padding:0 18px;margin:50px auto;width:500px"><tbody><tr width="100%" height="60"><td valign="top" align="left" style="border-top-left-radius:4px;border-top-right-radius:4px;background: white; padding:10px 18px;text-align:center"> <img height="75" width="75" src="https://cdn.discordapp.com/attachments/708550144827719811/792008916451328010/android-chrome-512x512.png" title="CGV" style="font-weight:bold;font-size:18px;color:#fff;vertical-align:top" class="CToWUd"></td></tr><tr width="100%"><td valign="top" align="left" style="background:#fff;padding:18px"><h1 style="font-size:20px;margin:16px 0;color:#333;text-align:center">India’s Largest Online Verification Network</h1><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333;text-align:center">Hey, ''' + str(
        name) + '''</p><div style="background:#f6f7f8;border-radius:3px"> <br><p style="font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;">We get it, stuff happens. Please use the link below to reset your password.</p><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;margin-bottom:0;text-align:center"> <a href="''' + link + '''" style="border-radius:3px;background:#3aa54c;color:#fff;display:block;font-weight:700;font-size:16px;line-height:1.25em;margin:24px auto 6px;padding:10px 18px;text-decoration:none;width:180px" target="_blank">Reset Password Now!</a></p> <br><br></div><p style="font:14px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333"> <strong>What's CGV?</strong> We generate and verify certificates online which also includes a backend dashboard. Click to know more. <a href="https://cgvcertify.herokuapp.com" style="color:#306f9c;text-decoration:none;font-weight:bold" target="_blank">Learn more »</a></p></td></tr></tbody></table></td></tr></tbody></table></body></html>'''
    content = content1
    message = Mail(
        from_email=('forgot-password@cgv.in.net', 'Password Bot CGV'),
        to_emails=email,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(json['sendgridapi'])
        response = sg.send(message)
        return True
    except Exception as e:
        print(e)
        return False


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password_page():
    if (request.method == 'POST'):
        email = request.form.get('email')
        post = Users.query.filter_by(email=email).first()
        name = post.name
        if (post != None):
            if (post.email == json["admin_email"]):
                flash("You can't reset password of administrator!", "danger")
            else:
                if send_password_reset_email(name, email):
                    flash(
                        f"We've sent a password reset link on {email}", "success")
                else:
                    flash("Error while sending password reset email!", "danger")
        elif (post == None):
            flash("We didn't find your account!", "danger")
            return render_template('forgot-password.html', json=json, verified=False)

    return render_template('forgot-password.html', json=json, verified=False)


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
        db.session.commit()
        flash('Password changed successfully.', 'success')
        return redirect(url_for('loginPage'))
    try:
        email = s.loads(token, salt="cgv-password-reset", max_age=1800)
    except SignatureExpired:
        flash("Sorry, link has been expired.", "error")
        return render_template('forgot-password.html', json=json, verified=False)
    except Exception:
        flash("Sorry, Invalid token.", "error")
        return render_template('forgot-password.html', json=json, verified=False)
    user = Users.query.filter_by(email=email).first()
    first_name = user.name.split(" ")[0]
    return render_template("forgot-password.html", json=json, name=first_name, token=token, verified=True)


@app.route('/view/mail', methods=['GET', 'POST'])
@login_required
def mail_page():
    if (request.method == 'POST'):
        fromemail = request.form.get('username')
        name = request.form.get('name')
        fromemail = fromemail + '@cgv.in.net'
        toemail = request.form.get('toemail')
        subject = request.form.get('subject')
        content = request.form.get('editordata')
        message = Mail(
            from_email=(fromemail, name),
            to_emails=toemail,
            subject=subject,
            html_content=content)
        try:
            sg = SendGridAPIClient(json['sendgridapi'])
            response = sg.send(message)
            flash("Email sent successfully!", "success")
        except Exception as e:
            print("Error")
            flash("Error while sending mail!", "danger")
    return render_template('mail.html', json=json, c_user_name=current_user.name, user=current_user)


@app.route('/')
def home_page():
    response = requests.get(json["contributors_api"])
    team = response.json()
    return render_template('index.html', json=json, team=team)


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('editordata')
        if (host == True):
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        else:
            ip_address = ipc
        # ip_address = ipc

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
        url = requests.get("http://ip-api.com/json/{}".format(ip_address))
        j = url.json()
        city = j["city"]
        country = j["country"]
        entry = Contact(name=name, phone=phone, message=message, ip=ip_address, city=city, country=country, date=time,
                        email=email)
        db.session.add(entry)
        db.session.commit()
        flash("Thank you for contacting us – we will get back to you soon!", "success")
    return redirect('/#footer')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        rating = request.form.get('rating')
        message = request.form.get('message')
        if (host == True):
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        else:
            ip_address = ipc
        url = requests.get("http://ip-api.com/json/{}".format(ip_address))
        j = url.json()
        city = j["city"]
        country = j["country"]
        entry = Feedback(name=name, phone=phone, rating=rating, message=message, ip=ip_address, city=city,
                         country=country, date=time, email=email)
        db.session.add(entry)
        db.session.commit()
        flash("Thank you for feedback – we will get back to you soon!", "success")
    return redirect('/#footer')


@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter_page():
    if (request.method == 'POST'):
        email = request.form.get('email')
        if (host == True):
            ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        else:
            ip_address = ipc
        url = requests.get("http://ip-api.com/json/{}".format(ip_address))
        j = url.json()
        city = j["city"]
        country = j["country"]
        post = Newsletter.query.filter_by(email=email).first()
        if (post == None):
            entry = Newsletter(ip=ip_address, city=city,
                               country=country, date=time, email=email)
            db.session.add(entry)
            db.session.commit()
            flash("Thank you for subscribing!", "success")
        else:
            flash("You have already subscribed!", "danger")
    return redirect('/#footer')


@app.route("/certificate/verify", methods=['GET', 'POST'])
def certificate_verify():
    if (host == True):
        # ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        ip_address = ipc
    else:
        ip_address = ipc
    if (request.method == 'POST'):
        certificate_no = request.form.get('certificateno')
        postc = Certificate.query.filter_by(number=certificate_no).first()
        if (postc != None):
            posto = Group.query.filter_by(id=postc.group_id).first()
            flash("Certificate Number Valid!", "success")
            return render_template('verify2.html', postc=postc, posto=posto, json=json, ip=ip_address)
        elif (postc == None):
            flash("No details found. Contact your organization!", "danger")
    return render_template('verify.html', json=json, ip=ip_address)


@app.route("/certificate/generate", methods=['GET', 'POST'])
def certificate_generate():
    # if (host == True):
    #     ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip_address = ipc
    ip_address = ipc
    if (request.method == 'POST'):
        certificateno = request.form.get('certificateno')
        postc = Certificate.query.filter_by(number=certificateno).first()
        if (postc != None):
            posto = Group.query.filter_by(id=postc.group_id).first()
            qr_code = QRCode.query.filter_by(
                certificate_num=certificateno).first()
            img_name = f"{qr_code.certificate_num}.png"
            return render_template('certificate.html', postc=postc, qr_code=img_name, posto=posto, json=json, ip=ip_address)
        elif (postc == None):
            flash("No details found. Contact your organization!", "danger")
    return render_template('generate.html', json=json, ip=ip_address)

import pdfkit

@app.route("/certify/<string:number>", methods=['GET'])
def certificate_generate_string(number):
    postc = Certificate.query.filter_by(number=number).first()
    if (postc != None):
        posto = Group.query.filter_by(id=postc.group_id).first()
        qr_code = QRCode.query.filter_by(certificate_num=number).first()
        img_name = f"{qr_code.certificate_num}.png"
        if app.debug:
            base_url = 'http://127.0.0.1:5000/'
        else:
            base_url = json["site_url"]
        rendered_temp = render_template('certificate.html', postc=postc, posto=posto, qr_code=img_name, json=json, number=number, pdf=True, base_url=base_url)
        try:
            pdfkit.from_string(rendered_temp, f'{number}.pdf', css='static/css/certificate.css')
        except OSError:
            pass
        return render_template('certificate.html', postc=postc, posto=posto, qr_code=img_name, json=json, number=number, pdf=False, base_url=base_url)
    else:
        return redirect('/')

@app.route('/download/<path:filename>', methods=['GET','POST'])
def download(filename):
    docs = os.path.join(current_app.root_path)
    return send_from_directory(directory=docs, filename=filename)


@app.route("/certifyd/<string:number>", methods=['GET'])
def certificate_generated_string(number):
    postc = Certificate.query.filter_by(number=number).first()
    if (postc != None):
        posto = Group.query.filter_by(id=postc.group_id).first()
        style = "display: none;"
        qr_code = QRCode.query.filter_by(certificate_num=number).first()
        img_name = f"{qr_code.certificate_num}.png"
        return render_template('certificate.html', postc=postc, posto=posto, qr_code=img_name, json=json, style=style)
    else:
        return redirect('/')


# Payment Views
@app.route("/pay", methods=["GET", "POST"])
def pay_now():
    print(request.form)
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
        print("payment Successfully done")
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
        print(remember)
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
            return render_template('login.html', json=json)
    else:
        return render_template('login.html', json=json)


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
    print(token)
    if app.debug:
        link = f"http://127.0.0.1:5000/confirm-email/{token}"
    else:
        link = f"{json['site_url']}/confirm-email/{token}"
    print(link)
    subject = "Welcome aboard " + name + "!"
    content1 = '''<!DOCTYPE html><html lang="en" ><head><meta charset="UTF-8"><title>Register CGV</title></head><body><table cellspacing="0" cellpadding="0" border="0" style="color:#333;background:#fff;padding:0;margin:0;width:100%;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><tbody><tr width="100%"><td valign="top" align="left" style="background:#eef0f1;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><table style="border:none;padding:0 18px;margin:50px auto;width:500px"><tbody><tr width="100%" height="60"><td valign="top" align="left" style="border-top-left-radius:4px;border-top-right-radius:4px;background: white; padding:10px 18px;text-align:center"> <img height="75" width="75" src="https://cdn.discordapp.com/attachments/708550144827719811/792008916451328010/android-chrome-512x512.png" title="CGV" style="font-weight:bold;font-size:18px;color:#fff;vertical-align:top" class="CToWUd"></td></tr><tr width="100%"><td valign="top" align="left" style="background:#fff;padding:18px"><h1 style="font-size:20px;margin:16px 0;color:#333;text-align:center">India’s Largest Online Verification Network</h1><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333;text-align:center">Hey, ''' + str(
        name) + '''</p><div style="background:#f6f7f8;border-radius:3px"> <br><p style="font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;">Thanks for signing up. Please use the link below to activate your account.</p><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;margin-bottom:0;text-align:center"> <a href="''' + link + '''" style="border-radius:3px;background:#3aa54c;color:#fff;display:block;font-weight:700;font-size:16px;line-height:1.25em;margin:24px auto 6px;padding:10px 18px;text-decoration:none;width:180px" target="_blank">Activate Now!</a></p> <br><br></div><p style="font:14px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333"> <strong>What's CGV?</strong> We generate and verify certificates online which also includes a backend dashboard. Click to know more. <a href="https://cgvcertify.herokuapp.com" style="color:#306f9c;text-decoration:none;font-weight:bold" target="_blank">Learn more »</a></p></td></tr></tbody></table></td></tr></tbody></table></body></html>'''
    content = content1
    message = Mail(
        from_email=('register-user@cgv.in.net', 'Register Bot CGV'),
        to_emails=email,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(json['sendgridapi'])
        response = sg.send(message)
        return True
    except Exception as e:
        print(e)
        return False


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
                      last_login=time, status=0, is_staff=1)
        db.session.add(entry)
        db.session.commit()
        if send_activation_email(name, email):
            flash(
                f"We've sent an account activation link on {email}", "success")
        else:
            flash("Error while sending account activation email!", "danger")
            return render_template('resend.html', json=json)
    return render_template('register.html', json=json)


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
    return render_template("resend.html", json=json)


@app.route('/confirm-email/<token>', methods=['GET'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    try:
        email = s.loads(token, salt="cgv-email-confirm", max_age=1800)
    except SignatureExpired:
        flash("Sorry, link has been expired.")
        return render_template('login.html', json=json)
    user = Users.query.filter_by(email=email).first()
    user.status = 1
    user.lastlogin = time
    db.session.commit()
    # Some error here
    if host:
        # ip_address = request.environ['HTTP_X_FORWARDED_FOR']
        ip_address = ipc
    else:
        ip_address = ipc
    url = requests.get("http://ip-api.com/json/{}".format(ip_address))
    j = url.json()
    city = j["city"]
    country = j["country"]
    html_text1 = '''<!DOCTYPE html><html lang="en" ><head><meta charset="UTF-8"><title>Login Alert</title></head><body><table cellspacing="0" cellpadding="0" border="0" style="color:#333;background:#fff;padding:0;margin:0;width:100%;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><tbody><tr width="100%"><td valign="top" align="left" style="background:#eef0f1;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><table style="border:none;padding:0 18px;margin:50px auto;width:500px"><tbody><tr width="100%" height="60"><td valign="top" align="left" style="border-top-left-radius:4px;border-top-right-radius:4px;background: white; padding:10px 18px;text-align:center"> <img height="75" width="75" src="https://cdn.discordapp.com/attachments/708550144827719811/792008916451328010/android-chrome-512x512.png" title="CGV" style="font-weight:bold;font-size:18px;color:#fff;vertical-align:top" class="CToWUd"></td></tr><tr width="100%"><td valign="top" align="left" style="background:#fff;padding:18px"><h1 style="font-size:20px;margin:16px 0;color:#333;text-align:center">Is that you?</h1><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333;text-align:center">We noticed you logged in to your CGV account from a new device and a new location.</p> <br><div style="background:#f6f7f8;border-radius:3px"> <br> City : '''
    html_final = html_text1 + str(city) + '''<br><br> Country : ''' + str(
        country) + '''<br><br>Time : ''' + str(time) + '''<br><br>IP : ''' + str(ip_address)
    html_text2 = '''<br><p>Tip: To keep your account secured, please contact us to update your email id. Ignore if it’s already updated.</p></div><br><p style="font:14px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333"> <strong>What's CGV?</strong> We generate and verify certificates online which also includes a backend dashboard. Click to know more. <a href="https://cgvcertify.herokuapp.com" style="color:#306f9c;text-decoration:none;font-weight:bold" target="_blank">Learn more »</a></p></td></tr></tbody></table></td></tr></tbody></table></body></html>'''
    html_final = html_final + html_text2
    subject = " New device login from " + \
        str(city) + ", " + str(country) + " detected."
    message = Mail(
        from_email=('login-alert@cgv.in.net', 'Security Bot CGV'),
        to_emails=email,
        subject=subject,
        html_content=html_final)
    try:
        sg = SendGridAPIClient(json['sendgridapi'])
        responsemail = sg.send(message)
    except Exception as e:
        print(e)
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
    print(current_user.name)
    return render_template('dashboard.html', json=json, postc=postc, postct=postct, postf=postf, postn=postn, user=current_user, )


@app.route("/view/groups", methods=['GET', 'POST'])
@login_required
def view_org_page():
    if current_user.is_staff:
        post = Group.query.order_by(Group.id).all()
        return render_template('org_table.html', post=post, json=json, user=current_user)
    else:
        return render_template('block.html', json=json, user=current_user)


@app.route("/view/users", methods=['GET', 'POST'])
@login_required
def view_users_page():
    if current_user.is_staff:
        post = Users.query.order_by(Users.id).all()
        return render_template('users_table.html', post=post, json=json, user=current_user)
    else:
        return render_template('block.html', json=json, user=current_user)


@app.route("/view/<string:grp_id>/certificates", methods=['GET', 'POST'])
@login_required
def view_certificate_page(grp_id):
    post = Certificate.query.filter_by(
        group_id=grp_id).order_by(Certificate.id)
    return render_template('certificate_table.html', post=post, json=json, c_user_name=current_user.name, user=current_user, grp_id=grp_id)


@app.route("/view/contacts", methods=['GET', 'POST'])
@login_required
def view_contacts_page():
    post = Contact.query.order_by(Contact.id).all()
    return render_template('contact_table.html', post=post, json=json, c_user_name=current_user.name, user=current_user)


@app.route("/view/feedbacks", methods=['GET', 'POST'])
@login_required
def view_feedbacks_page():
    post = Feedback.query.order_by(Feedback.id).all()
    return render_template('feedback_table.html', post=post, json=json, c_user_name=current_user.name, user=current_user)


@app.route("/view/newsletters", methods=['GET', 'POST'])
@login_required
def view_newsletters_page():
    post = Newsletter.query.order_by(Newsletter.id).all()
    return render_template('newsletter_table.html', post=post, json=json, c_user_name=current_user.name, user=current_user)


@app.route("/view/messages/<string:id>", methods=['GET'])
@login_required
def view_message_page(id):
    post = Contact.query.filter_by(id=id).first()
    return render_template('view_message.html', post=post, json=json, c_user_name=current_user.name, user=current_user)


@app.route("/edit/<string:grp_id>/certificates/<string:id>", methods=['GET', 'POST'])
@login_required
def edit_certificates_page(grp_id, id):
    if request.method == 'POST':
        data = json_lib.loads(request.data)
        name = data["name"]
        coursename = data["course"]
        email = data["email"]
        letters = string.ascii_letters
        number = ''.join(random.choice(letters) for i in range(4))
        number = 'CGV' + name[0:4].upper() + number
        userid = current_user.id
        last_update = time
        if id == '0':
            postcheck = Certificate.query.filter_by(
                email=email, coursename=coursename).first()
            if (postcheck == None):
                try:
                    post = Certificate(name=name, number=number, email=email, coursename=coursename, user_id=userid,
                                       group_id=grp_id, last_update=last_update)
                    db.session.add(post)
                    # Create QR Code for this certificate
                    link = f'{json["site_url"]}/certify/{number}'
                    new_qr = QRCode(certificate_num=number, link=link)
                    qr_image = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr_image.add_data(link)
                    qr_image.make(fit=True)
                    img = qr_image.make_image(fill='black', back_color='white')
                    imgname = f"{number}.png"
                    try:
                        os.mkdir("static/qr_codes")
                    except Exception:
                        pass
                    img.save("static/qr_codes/"+imgname)
                    new_qr.qr_code = f"qr_codes/{imgname}"
                    db.session.add(new_qr)
                    db.session.commit()
                    subject = "Certificate Generated With Certificate Number : " + \
                        str(number)
                    content1 = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Certificate Download</title></head><body><table cellspacing="0" cellpadding="0" border="0" style="color:#333;background:#fff;padding:0;margin:0;width:100%;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><tbody><tr width="100%"><td valign="top" align="left" style="background:#eef0f1;font:15px/1.25em 'Helvetica Neue',Arial,Helvetica"><table style="border:none;padding:0 18px;margin:50px auto;width:500px"><tbody><tr width="100%" height="60"><td valign="top" align="left" style="border-top-left-radius:4px;border-top-right-radius:4px;background: white; padding:10px 18px;text-align:center"> <img height="75" width="75" src="https://cdn.discordapp.com/attachments/708550144827719811/792008916451328010/android-chrome-512x512.png" title="CGV" style="font-weight:bold;font-size:18px;color:#fff;vertical-align:top" class="CToWUd"></td></tr><tr width="100%"><td valign="top" align="left" style="background:#fff;padding:18px"><h1 style="font-size:20px;margin:16px 0;color:#333;text-align:center">India’s Largest Online Verification Network</h1><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333;text-align:center">Hey, ''' + str(
                        name)
                    content2 = '''</p><div style="background:#f6f7f8;border-radius:3px"> <br><p>Congratulations! Your certificate has been issued successfully.</p><p>Certificate Number : ''' + str(
                        number)
                    content3 = '''</p><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;margin-bottom:0;text-align:center"> <a href="https://''' + \
                        json["site_url"] + '''/certify/''' + str(
                            number) + '''" style="border-radius:3px;background:#3aa54c;color:#fff;display:block;font-weight:700;font-size:16px;line-height:1.25em;margin:24px auto 6px;padding:10px 18px;text-decoration:none;width:215px" target="_blank"> Download Certificate Here!</a><p style="font:15px/1.25em 'Helvetica Neue',Arial,Helvetica;margin-bottom:0;text-align:center"> <a href="''' + \
                        json[
                            "site_url"] + '''/certificate/verify" style="border-radius:3px;background:#3aa54c;color:#fff;display:block;font-weight:700;font-size:16px;line-height:1.25em;margin:24px auto 6px;padding:10px 18px;text-decoration:none;width:215px" target="_blank"> E-Verify Certificate Here!</a></p> <br> <br></div><p style="font:14px/1.25em 'Helvetica Neue',Arial,Helvetica;color:#333"> <strong>What's CGV?</strong> We generate and verify certificates online which also includes a backend dashboard. Click to know more. <a href="https://cgvcertify.herokuapp.com" style="color:#306f9c;text-decoration:none;font-weight:bold" target="_blank">Learn more »</a></p></td></tr></tbody></table></td></tr></tbody></table></body></html>'''
                    content = content1 + content2 + content3
                    message = Mail(
                        from_email=('certificate-generate@cgv.in.net',
                                    'Certificate Generate Bot CGV'),
                        to_emails=email,
                        subject=subject,
                        html_content=content)
                    try:
                        sg = SendGridAPIClient(json['sendgridapi'])
                        response = sg.send(message)
                    except Exception as e:
                        print("Error!")
                        flash("Error while sending mail!", "danger")
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
    return jsonify(json=json, id=id, post=post)


@app.route("/activate/user/<string:id>", methods=['GET', 'POST'])
@login_required
def activate_users(id):
    activate = Users.query.filter_by(id=id).first()
    if (activate.email == json["admin_email"]):
        flash("Administrator account will always be active!", "warning")
        return redirect(url_for('view_users_page'))
    else:
        if (activate.status == 1):
            activate.status = 0
            flash("User account deactivated!", "warning")
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


@app.route("/edit/group/<string:id>", methods=['GET', 'POST'])
@login_required
def edit_org_page(id):
    if request.method == 'POST':
        data = json_lib.loads(request.data)
        name = data["name"]
        dept = data["dept"]
        email = data["email"]
        phone = data["phone"]
        date = time
        if id == '0':
            if Group.query.filter_by(email=email).first():
                return jsonify(group_duplicate=True)
            try:
                post = Group(name=name, subname=dept, email=email,
                             phone=phone, date=date, user_id=current_user.id)
                db.session.add(post)
                db.session.commit()
                return jsonify(group_success=True)
            except Exception:
                return jsonify(group_error=True)

        else:
            try:
                post = Group.query.filter_by(id=id).first()
                post.name = name
                post.subname = dept
                post.phone = phone
                post.email = email
                post.date = date
                post.user_id = current_user.id
                db.session.commit()
                return jsonify(group_success=True)
            except Exception:
                return jsonify(group_error=True)
    grp = Group.query.filter_by(id=id).first()
    post = {
        "id": grp.id,
        "name": grp.name,
        "subname": grp.subname,
        "email": grp.email,
        "phone": grp.phone
    }
    return jsonify(json=json, id=id, post=post)


@app.route("/delete/group/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_org_page(id):
    delete_org_page = Group.query.filter_by(id=id).first()
    if (delete_org_page.email == json["admin_email"]):
        flash("Default organization can't be deleted!", "danger")
    else:
        db.session.delete(delete_org_page)
        db.session.commit()
        flash("Organization deleted successfully!", "success")
    return redirect('/view/groups')


@app.route("/delete/users/<string:id>", methods=['GET', 'POST'])
@login_required
def delete_users_page(id):
    delete_users_page = Users.query.filter_by(id=id).first()
    if (delete_users_page.email != json["admin_email"]):
        db.session.delete(delete_users_page)
        db.session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("You can't delete administrator!", "danger")
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

    print(f"I am base url {request.base_url}")

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
    pwo = PasswordGenerator()
    pwd = pwo.generate()
    password = sha256_crypt.hash(pwd)
    # Create a user in your db with the information provided
    # by Google

    # Doesn't exist? Add it to the database.
    if not Users.query.filter_by(email=users_email).first():
        entry = Users(name=users_name, email=users_email, password=password,
                      profile_image=picture, lastlogin=time, createddate=time, status=1)
        db.session.add(entry)
        db.session.commit()

    # Begin user session by logging the user in

    user = Users.query.filter_by(email=users_email).first()
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("dashboard_page"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def user_not_authorized(e):
    return render_template('401.html'), 401


if __name__ == '__main__':
    app.run()
