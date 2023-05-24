import os
from flask import Flask, render_template, redirect, abort, request, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# import sqlite3
import json

# APP CONTEXT -- NASA FLASA

app = Flask(__name__)


class MojFormular(FlaskForm):
    info = StringField("info", validators=[DataRequired(message="REQUIRED")])
    pwd = PasswordField("Password")
    submit = SubmitField("Submit")

app.config["SECRET_KEY"] = os.urandom(32)
app.config["CSRF_ENABLED"] = True   # Cross Site Request Forgery

login_manager = LoginManager()
login_manager.init_app(app)

# Mock
users = {"andrej@gmail.com":{"password":"halabal"}, "filip@gmail.com":{"password":"netusim"}}


class User(UserMixin):
    pass


# LOGIN MANAGER LOADER

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return '''
        <form action="login" method="POST">
        <input type="text" name="email" id="email" placeholder="email"</input>
        <input type="password" name="password" id="password" placeholder="password"</input>
        <input type="submit" name="submit"</input>
        </form>
        '''
    email = request.form["email"]
    print(request.form)
    if email in users and request.form["password"] == users[email]["password"]:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for("protected"))
    return "<h2>BAD LOGIN</h2>"

@app.route("/protected")
@login_required
def protected():
    return "NALOGOVANY AKO UZIVATEL" + current_user.id

@app.route("/logout")
def logout():
    logout_user()
    return "ODHLASENY UZIVATEL"



# ROUTES
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/setsession")
def setsession():
    session["USERNAME"] = "Anonymous"
    flash("USERNAME JE NASTAVENE")
    app.logger.debug("USERNAME JE NASTAVENE")
    return redirect("/index")

@app.route("/getsession")
def getsession():
    if "USERNAME" in session:
        username = session["USERNAME"]
        msg = f"SESSION FOR USER : {username} WAS ACCESED"
        flash(msg)
        app.logger.info(msg)
        return redirect("/index")
    else:
        return "<h1>WELCOME GUEST</h1>"

@app.route("/delsession")
def delsession():
    session.pop("USERNAME", None)
    flash("SESSION BOLA VYMAZANA")
    app.logger.debug("SESSION BOLA VYMAZANA")
    return redirect("/index")

@app.route("/submit", methods=["GET"])
def submit():
    return render_template("submit.html")

@app.route("/info", methods=["GET", "POST"])
def info():
    form = MojFormular()
    app.logger.debug("FORMULAR BOL VYTVORENY")
    if request.method == "POST":
        csrf.generate_csrf()
        app.logger.debug("SPRAVA PRISLA")
        if form.validate():
            print(request.form.get("pwd"))
            # info_list.append(request.form.get("info"))
            session["info"] = request.form["info"]
            # with open(file="session_info.json", mode="a", encoding="utf8") as f:
            #     json.dump(fp=f, obj=session, indent=4)
            # add_record(session["info"])
            app.logger.debug("SPRAVA BOLA ULOZENA")
        return redirect("/submit")
    else:
        app.logger.debug("SPRAVA NEBOLA ULOZENA")

    form = MojFormular()
    app.logger.debug("FORMULAR BOL VYTVORENY")
    return render_template("info.html", form=form)

@app.route("/view", methods=["GET"])
def infolist():
    try:
        entry = str(session["info"])
        app.logger("SPRAVA")
        flash("Info je v poriadku")
    except KeyError:
        entry = None
        flash("NEMAM INFO")
    finally:
        return render_template("view.html", entry=entry)


if __name__ == "__main__":
    app.run(debug=True)