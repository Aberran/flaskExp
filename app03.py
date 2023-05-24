import os
from flask import Flask, render_template, redirect, abort, request, session, flash
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# APP CONTEXT -- NASA FLASA

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["CSRF_ENABLED"] = True   # Cross Site Request Forgery

# ULOZISTE DAT
info_list = ["test1", "test2", "test3"]

# FORMULAR
class MojFormular(FlaskForm):
    info = StringField("info", validators=[DataRequired(message="REQUIRED")])
    submit = SubmitField("Submit")

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




""" VERZIA 2
@app.route("/info", methods=["GET", "POST"])
def info():
    if request.method == "POST":
        print(request.form.get("info"))
        info_list.append("INFO ULOZENA")
    form = MojFormular()
    app.logger.debug("FORMULAR BOL VYTVORENY")
    return render_template("info.html", form=form)
"""
"""
@app.route("/info", methods=["GET"])
def info_get():
    form = MojFormular()
    app.logger.debug("FORMULAR BOL VYTVORENY")
    return render_template("info.html", form=form)

@app.route("/info", methods=["POST"])
def info_post():
    if request.method == "POST":
        print(request.form.get("info"))
        info_list.append("INFO ULOZENA")
        return redirect("/submit")
"""
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
            print(request.form.get("info"))
            # info_list.append(request.form.get("info"))
            session["info"] = request.form["info"]
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