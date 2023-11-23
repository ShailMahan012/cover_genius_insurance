#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import paypal as PAYPAL
from paypal_config import paypal as paypal_config
import logging

app = Flask(__name__)
app.secret_key = "mysecretkey"
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.app_context().push()


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    address = db.Column(db.Text)
    phone = db.Column(db.Text)
    paid = db.Column(db.Boolean, default=False, nullable=False)

    vehicle_model = db.Column(db.Text)
    vehicle_year = db.Column(db.Integer)


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

        user = Users(first_name=first_name, last_name=last_name, email=email, address=address, phone=phone)
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
            user.vehicle_model = data["model"]
            user.vehicle_year = data["year"]
            db.session.commit()
            return "true"
    return "false"


@app.route("/payment")
def payment():
    user_id = session.get("user_id")
    if user_id is None or user_id == -1:
        return redirect("/signup")
    user = db.session.get(Users, user_id)
    return render_template("payment.html", email=user.email, CLIENT_ID=paypal_config["CLIENT_ID"])


@app.route("/paypal/create_order")
def create_order():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/signup")
    resp = PAYPAL.create_order(user_id)
    return resp


@app.route("/paypal/capture_order/<order_id>", methods=["POST"])
def capture_order(order_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/signup")

    response, response_code = PAYPAL.capture_payment(order_id)
    if response_code in (200, 201):
        user = db.session.get(Users, user_id)
        if user:
            user.paid = True
            db.session.commit()
        else:
            print("User not found:", user_id)

    return response, response_code


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

