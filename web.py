#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import stripe
from stripe_config import stripe_config
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecretkey"
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.app_context().push()
domain = ('https', "autocoverltd.com")
domain = ('http', "localhost:5050")
stripe.api_key = stripe_config['KEY']


@app.context_processor
def inject_domain():
    return dict(domain=domain[1])


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    address = db.Column(db.Text)
    phone = db.Column(db.Text)
    paid = db.Column(db.Boolean, default=False, nullable=False)

    vehicle_type = db.Column(db.Text)
    dob = db.Column(db.Date)

    ip = db.Column(db.Text)


def get_ip():
    ip = request.headers.get('X-Forwarded-For')
    if not ip:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return ip


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        phone = request.form.get("phone")

        user = Users(first_name=first_name, last_name=last_name, email=email, address=address, phone=phone, ip=get_ip())
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect("/get_covered")
    return render_template("signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id") == -1:
        return redirect("/admin")
    if request.method == "POST":
        username = request.form.get("autocover_username")
        password = request.form.get("password")
        if username == "admin" and password == "admin@012":
            session["user_id"] = -1
            return redirect("/admin")
        flash("Incorrect information", "danger")
    return render_template("admin_login.html")


@app.route("/get_covered")
def get_covered():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/signup")
    return render_template("get_covered.html")


@app.route("/save_vehicle", methods=["POST"])
def save_vehicle():
    user_id = session.get("user_id")
    if user_id:
        user = db.session.get(Users, user_id)
        if user:
            data = request.json
            date = data.get("dob").split("-")
            date = tuple(map(int, date))
            date = datetime(date[0], date[1], date[2])
            user.dob = date
            user.vehicle_type = data.get("vehicle_type")
            db.session.commit()
            return "true"
    return "false"


@app.route("/payment")
def payment():
    user_id = session.get("user_id")
    user = db.session.get(Users, user_id)
    if user_id is None or user_id == -1 or user is None:
        return redirect("/signup")
    return render_template("payment.html", email=user.email, payed=user.paid)


@app.route('/create-checkout-session')
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': stripe_config['PRD_ID'],
                    'quantity': stripe_config['QUANTITY'],
                },
            ],
            mode='payment',
            success_url = f'{domain[0]}://{domain[1]}/yfufcn1qqt',
            cancel_url = f'{domain[0]}://{domain[1]}/payment',
        )
    except Exception as e:
        print(e)
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route("/yfufcn1qqt")
def accept_payment():
    user_id = session.get("user_id")
    if user_id:
        user = db.session.get(Users, user_id)
        user.paid = True
        db.session.commit()
        return redirect("/payment")
    return redirect("/signup")


@app.route("/admin")
def admin():
    if (session.get("user_id") != -1):
        flash("Login Please", "danger")
        return redirect("/login")
    return render_template("admin.html", users=Users.query.all())


@app.route("/logout")
def logout():
    user_id = session.get("user_id")
    if user_id:
        session.pop("user_id")
        if user_id == -1:
            return redirect("/login")
    return redirect("/signup")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

