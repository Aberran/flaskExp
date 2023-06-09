from flask import Flask, render_template, abort, redirect, request
import datetime

app = Flask(__name__)

BUFFER = list()
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 404

# ROUTES

@app.route("/")
@app.route("/index")

def main():
    return "<h1>AHOJ JA SOM DZIN Z FLASKU</h1>"

@app.route("/mojastranka")
def moja():
    return"<h2>Test mojej stranky</h2><br><p>toto je moja skusobna stranka</p>"

@app.route("/vitajte")
def welcome():
    return render_template("vitajte.html")

@app.route("/welcome")
def vitajte():
    return redirect("/vitajte")

@app.route("/cas")
def cas():
    return render_template("main.html", cas=datetime.datetime.now())

@app.route("/spravy/<int:index>", methods=["GET"])
def spravy(index):
    spravy = ["sprava1", "sprava2", "sprava3"]
    try:
        return render_template("spravy.html", msg=spravy[index])
    except IndexError:
        abort(404)

@app.route("/kurzkk", methods=["GET"])
def kurz():
    kurz = [12, 34, 23, 78, 45, -5, -78, 14, 45, 33]
    return render_template("kurzkk.html", kurzy=kurz)

# ///////////////////////////////////

@app.route("/form", methods=["GET", "POST"])
def form():
    print(request)
    if request.method == "POST":
        user = request.form.get("user")
        pwd = request.form.get("pwd")
        print(user, pwd)
        BUFFER.append((user,pwd)) # pridavame tuple
        app.logger.info("USPECH - Vysledok formulara bol ulozeny do BUFFERU")


    return render_template("form.html", form=form)





if __name__ == "__main__":
    app.run(debug=True)

# DEVELOPMENT -> DEVOPS -> PRODUKCNY SERVER

