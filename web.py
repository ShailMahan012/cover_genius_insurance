#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
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
    password = db.Column(db.Text)
    phone = db.Column(db.Text)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")

        user = Users.query.filter_by(email=email).first()
        if not user:
            user = Users(first_name=first_name, last_name=last_name, email=email, password=password, phone=phone)
            db.session.add(user)
            db.session.commit()
            return redirect("/get_covered")
        flash("Email already in use", "danger")
    return render_template("signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect("/get_covered")
        flash("Incorrent Information", "danger")
    return render_template("login.html")


@app.route("/get_covered")
def get_covered():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    return render_template("get_covered.html")


@app.route("/payment")
def payment():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    user = db.session.get(Users, user_id)
    return render_template("payment.html", email=user.email)


@app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

